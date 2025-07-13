import json
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from fake_headers import Headers
import requests
import lxml

from playwright_parser import BrowserClient
from json_manager import Manager

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

def get_response(url: str):
    headers = Headers('chrome', 'win', headers=True).generate()
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print('Response was returned with a status of 400 or more.')
        return False
    else:
        return response.text


def get_item_data(url: str):
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
            print(f'{data}\n{url} -> repeat request.')
            return get_item_data(url)

    except Exception as e:
        raise ValueError(f"Parser error: \n{e}")


def main():
    json_mng = Manager()
    if not json_mng.isFile:
        try:
            soup = BeautifulSoup(get_response(DOMAIN + MENU), 'lxml')
            html_menu_items = soup.find_all('li', class_ = 'cmp-category__item')
            
            urls = []
            for item in html_menu_items:
                item: BeautifulSoup
                urls.append(DOMAIN + item.find('a').get('href'))
            
            with ThreadPoolExecutor(max_workers=5) as executer:
                result = list(executer.map(get_item_data, urls))
            return json_mng.manage_file(result)
            # return json_mng.manage_file([get_item_data(urls[1])])
            
        except Exception as e:
            raise ValueError(f"Parser error: \n{e}")
    else:
        return json_mng.manage_file()


if __name__ == "__main__":
    from time import time
    start = time()
    main()
    end = time()
    print('Program worked: ', end - start)