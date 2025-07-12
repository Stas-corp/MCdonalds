import json
# import threading
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from fake_headers import Headers
import requests
import lxml

from playwright_parser import BrowserClient

DOMAIN = 'https://www.mcdonalds.com'
MENU = '/ua/uk-ua/eat/fullmenu.html'
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(response.text)

def get_response(url: str):
    headers = Headers('chrome', 'win', headers=True).generate()
    response = requests.get(url, headers=headers)
    if response.status_code >= 400:
        print('Response was returned with a status of 400 or more.')
        return False
    else:
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(response.text)
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
    except:
        raise ValueError("Parser error")
    # print(url, 'OK')
    
    # pimary_item = soup.find_all('li', class_ = 'cmp-nutrition-summary__heading-primary-item')
    # second_item = soup.find('div', class_ = 'cmp-nutrition-summary__details-column-view-desktop')
    
    data = {
        'name': soup.find('h1').text.strip(),
        'descreption': soup.find('div', class_ = 'cmp-product-details-main__description').text.strip().replace('\xa0', ' ')
    }
    
    # btn = soup.find("button", id="accordion-29309a7a60-item-9ea8a10642-button")
    # panel_id = btn.get("aria-controls")
    # panel = soup.find(id=panel_id)
    
    print(data)
    browser.close()


def main():
    try:
        soup = BeautifulSoup(get_response(DOMAIN + MENU), 'lxml')
    except:
        raise ValueError("Parser error")
    
    html_menu_items = soup.find_all('li', class_ = 'cmp-category__item')
    
    urls = []
    for item in html_menu_items:
        item: BeautifulSoup
        urls.append(DOMAIN + item.find('a').get('href'))
    
    with ThreadPoolExecutor(max_workers=5) as executer:
        executer.map(get_item_data, urls)
    # get_item_data(urls[0], browser)
    


if __name__ == "__main__":
    from time import time
    start = time()
    main()
    end = time()
    print('Program worked: ', end - start)