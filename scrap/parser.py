import json
import threading
from concurrent.futures import ThreadPoolExecutor


from bs4 import BeautifulSoup
from fake_headers import Headers
import requests
import lxml

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
        return response.text


def get_item_data(url: str):
    try:
        soup = BeautifulSoup(get_response(url), 'lxml')
    except:
        raise ValueError("Parser error")
    print(url, 'OK')


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
        
    with ThreadPoolExecutor(max_workers=3) as executer:
        executer.map(get_item_data, urls)
    
    
if __name__ == "__main__":
    main()