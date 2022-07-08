from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.headless = False
chrome_options.add_argument('--allow-profiles-outside-user-dir')
chrome_options.add_argument('--enable-profile-shortcut-manager')
chrome_options.add_argument(r'user-data-dir=%s\profiles\%s' % (os.getcwd(), 0))
chrome_options.add_argument('--profile-directory=Profile')
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
driver.create_options()
#driver.get('https://www.google.com/search?q=site:minsk-region.by&sxsrf=APq-WBuDzB1AMuFNFq9vl9YDsKBvp0R7cg:1651032849712&ei=EcNoYtL1KuqUxc8PjMevmA4&start=0&sa=N&ved=2ahUKEwiSwpPUsLP3AhVqSvEDHYzjC-M4ChDy0wN6BAgBEDw&cshid=1651032980772887&biw=899&bih=760&dpr=1')


def parse_page(number_page):
    print('Страница: %s' % (number_page // 10))
    driver.get('https://www.google.com/search?q=site:minsk-region.by&sxsrf=APq-WBuDzB1AMuFNFq9vl9YDsKBvp0R7cg:1651032849712&ei=EcNoYtL1KuqUxc8PjMevmA4&start=%s&sa=N&ved=2ahUKEwiSwpPUsLP3AhVqSvEDHYzjC-M4ChDy0wN6BAgBEDw&cshid=1651032980772887&biw=899&bih=760&dpr=1' % number_page)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    tabs = page.find_all('div', class_='jtfYYd')
    data_page = [[i.find('h3', class_='LC20lb MBeuO DKV0Md').text,
                  i.find('a')['href'],
                  i.find('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf').text]
                 for i in tabs]
    return data_page
if __name__ == "__main__":
    number = 0
    data = []
    while True:
        try:
            page = parse_page(number)
            if page == []:
                break
            for i in page:
                data.append(i)
        except Exception as e:
            print(e)
            break
        number += 10
    print(data)
    with open('out.txt', 'w', encoding='utf-8') as file:
        text = ''
        for i in data:
            text+='%s | %s | %s\n' % (i[0], i[1], i[2])
        file.write(text)