import json
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from fake_headers import Headers
from yaspin import yaspin, Spinner
import requests
import lxml

from scrap.playwright_parser import BrowserClient
from scrap.json_manager import Manager

DOMAIN = 'https://www.mcdonalds.com'
MENU = '/ua/uk-ua/eat/fullmenu.html'
KEYS = [
    "calories",
    "fats",
    "carbs",
    "proteins",
    "unsaturated_fats",
    "sugar",
    "salt",
    "portion"
]

json_mng = Manager()

def get_response(url: str) -> str | bool:
    headers = Headers('chrome', 'win', headers=True).generate()
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print('Response was returned with a status of 400 or more.')
        return False
    else:
        return response.text


def get_item_data(url: str) -> dict:
    '''Parses nutritional and product details from the given URL.
    
    Extracts main and secondary nutritional info, handles missing keys with a retry.
    
    '''
    browser = BrowserClient()
    html = browser.get_page_html(
        url,
        click_selector="#accordion-29309a7a60-item-9ea8a10642-button",
        wait_selector="#accordion-29309a7a60-item-9ea8a10642-panel"
    )
    
    try:
        soup = BeautifulSoup(html, 'lxml')
        pimary_items = soup.find_all('li', class_ = 'cmp-nutrition-summary__heading-primary-item')
        second_items = soup.find('div', class_ = 'cmp-nutrition-summary__details-column-view-desktop')
        second_items = second_items.find_all('li', class_ = 'label-item')

        data = {
            'name': soup.find('h1').text.strip(),
            'descreption': soup.find('div', class_ = 'cmp-product-details-main__description').text.strip().replace('\xa0', ' ')
        }
        
        for item, key in zip(pimary_items, KEYS[:5]):
            target = item.find('span', class_=False).text.strip()
            data[key] = target
        
        for item, key in zip(second_items, KEYS[4:]):
            target = item.find('span', class_=False).text.strip().split('\n')
            data[key] = target[0]
            
        browser.close()
        
        try:
            assert KEYS == list(data.keys())[2:]
            return data
        except:
            print(f'{url} -> repeat request.')
            return get_item_data(url)

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
                soup = BeautifulSoup(get_response(DOMAIN + MENU), 'lxml')
                html_menu_items = soup.find_all('li', class_ = 'cmp-category__item')
                
                urls = []
                for item in html_menu_items:
                    item: BeautifulSoup
                    urls.append(DOMAIN + item.find('a').get('href'))
                
                with ThreadPoolExecutor(max_workers=5) as executer:
                    result = list(executer.map(get_item_data, urls))
                    
                spinner.ok("✔")
                return json_mng.manage_file(result)
                # return json_mng.manage_file([get_item_data(urls[1])])
            
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