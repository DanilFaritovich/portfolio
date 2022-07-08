import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

ua = UserAgent()
userAgent = ua.chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.headless = False
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
driver.create_options()


def parse_main_links(url):
    driver.get(url)
    time.sleep(10000000)
    last_height = driver.execute_script("return document.body.scrollHeight")
    n = 18
    while True:
        len_list = len(driver.find_elements(by=By.XPATH, value='//div[@class="q-box qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-bg--raised"]//div//div//span//a'))
        if len_list >= 500:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height
        print(len_list)
    all_links = []
    page = BeautifulSoup(driver.page_source, 'html.parser')
    main_block = driver.find_elements(by=By.XPATH, value='//div[@class="q-box qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-bg--raised"]//div//div//span//a')[:501]
    for element in main_block:
        try:
            all_links.append(element.get_attribute('href'))
        except:
            all_links.append('None')
    return all_links


if __name__ == "__main__":
    list_main_links = parse_main_links('https://www.quora.com/search?q=thailand')
    print(len(list_main_links))
    for i in list_main_links:
        print(i)
    a = pd
    df = a.DataFrame(list_main_links, columns=['links'])
    writer = a.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Лист 1', index=False)
    # workbook = writer.book
    worksheet = writer.sheets['Лист 1']
    worksheet.set_column('A:A', 20)
    writer.save()