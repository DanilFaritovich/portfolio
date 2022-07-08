import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_catalog(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return [category['href']
            for category in soup.find('ul', id='menu-1-eb96a68').find_all('a')]


def parse_elements(url):
    def check_price(price):
        try:
            return price.find('div', class_='product_price').text.replace('р', ' ₽').replace(' за 1 Кг', '')
        except:
            return price.find('bdi').text.replace('\xa0', ' ')

    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    сolumn = soup.find('ul', class_='products columns-1')

    elements_list = []
    for element in сolumn.find_all('li'):
        name = element.find('h2').text

        try:
            price = element.find('div', class_='product_price').text.replace('р', ' ₽').replace(' за 1 Кг', '').replace(' / кг', '').replace(' / шт', '').replace(' / контакт', '').replace(' / секция', '').replace('Состояние:Новый', '').replace('Состояние:Б/у', '').replace('зап ₽осу', 'запросу').replace('П ₽ове ₽ка ', 'Проверка')
            if 'Паспо ₽т:' in price:
                print(price)
                price = '.'.join(price.split('.')[-2:])
                print(price)
        except:
            price = element.find('bdi').text.replace('\xa0', ' ')

        element_url = element.find('div', class_='product_thumbnail')['style'].replace('background:url(', '').replace(') no-repeat center, #000;background-size:cover;', '')
        if element_url == '':
            element_url = 'None'

        elements_list.append([name, price, element_url])
    return elements_list


if __name__ == '__main__':
    catalog = parse_catalog('https://zakypaem.ru/catalog/')

    result_list = []
    for category in catalog:
        result_list.append(parse_elements(category))
    result_list = [b
                   for i in result_list
                   for b in i]
    a = pd
    df = a.DataFrame(result_list, columns=['Наименование', 'Цена', 'Ссылка на изображение'])
    writer = a.ExcelWriter('res.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Лист 1', index=False)
    worksheet = writer.sheets['Лист 1']
    worksheet.set_column('A:C', 20)
    writer.save()
