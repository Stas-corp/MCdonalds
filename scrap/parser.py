import json
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from fake_headers import Headers
from yaspin import yaspin, Spinner
import requests
import lxml

from scrap.json_manager import Manager


DOMAIN = 'https://www.mcdonalds.com'
MENU = '/ua/uk-ua/eat/fullmenu.html'
ITEMS = '/dnaapp/itemDetails?country=UA&language=uk&showLiveData=true&item='
KEYS = [
    "portion",
    "calories",
    "fats",
    "unsaturated_fats",
    "carbs",
    "sugar",
    "proteins",
    "salt"
]

json_mng = Manager()

def get_response(url: str) -> requests.Response | bool:
    headers = Headers('chrome', 'win', headers=True).generate()
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print('Response was returned with a status of 400 or more.')
        return False
    else:
        return response


def get_item_data(id: str) -> dict:
    '''Parses nutritional and product details from the given ID.
    
    Extracts main and secondary nutritional info, handles missing keys with a retry.
    
    '''
    try:
        all_data = get_response(DOMAIN + ITEMS + id).json()['item']
        nutrient = all_data['nutrient_facts']['nutrient']
        data = {
            'name': all_data['item_name'],
            'descreption': all_data['description'],
        }
        
        shift = 0
        for i, nut in enumerate(nutrient):
            i -= shift
            if nut['name'] == 'Ен. Цінність, кДж':
                shift += 1
                continue
            data[KEYS[i]] = f"{nut['value']} {nut['uom']}"
            
        return data

    except Exception as e:
        raise ValueError(f"Parser error: \n{e}")


def main() -> dict:
    '''## Main function to collect product data from the menu page.
    
    If local JSON file doesn't exist, it scrapes all product pages in parallel,
    saves the result, and returns it. Otherwise, loads data from the existing file.
    
    '''
    if not json_mng.isFile:
        try:
            with yaspin(Spinner('-\\|/', 550), "Parsing menu items...", color="cyan") as spinner:
                response = get_response(DOMAIN + MENU).text
                soup = BeautifulSoup(response, 'lxml')
                html_menu_items = soup.find_all('li', class_ = 'cmp-category__item')
                
                list_id = []
                for item in html_menu_items:
                    item: BeautifulSoup
                    list_id.append(item.get('data-product-id'))
                
                with ThreadPoolExecutor(max_workers=5) as executer:
                    result = list(executer.map(get_item_data, list_id))
                    
                spinner.ok("✔")
                return json_mng.manage_file(result)
                # return json_mng.manage_file([get_item_data(list_id[1])])
                # get_item_data(list_id[1])
            
        except Exception as e:
            raise ValueError(f"Parser error: \n{e}")
    else:
        return json_mng.manage_file()


if __name__ == "__main__":
    from time import time
    start = time()
    print(main())
    end = time()
    print('Program worked: ', end - start)