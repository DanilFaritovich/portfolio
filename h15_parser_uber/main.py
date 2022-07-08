import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import re
import db_creater


def search_price(driver):
    try:
        driver.get('http://ubertarif.ru/')
        driver.find_element(By.XPATH, '//input[@id="pickupKey"]').send_keys('улица Академика Королева, 4, Набережные Челны')
        time.sleep(3)
        driver.find_elements(By.XPATH, '//div[@class="ui-menu-item-wrapper"]')[0].click()
        driver.find_element(By.XPATH, '//input[@id="dropoffKey"]').send_keys('проспект Московский, 129/5, Набережные Челны')
        time.sleep(3)
        driver.find_elements(By.XPATH, '//div[@class="ui-menu-item-wrapper"]')[1].click()
        driver.find_element(By.XPATH, '//input[@id="getroute"]').click()
    except Exception as e:
        time.sleep(10)
        search_price(driver)

def search_weather(driver):
    try:
        driver.get('https://www.gismeteo.ru/weather-naberezhnye-chelny-4534/now/')
    except Exception as e:
        time.sleep(5)
        search_weather(driver)

ua = UserAgent()
userAgent = ua.random
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.headless = False
#chrome_options.add_argument('--proxy-server=5.188.45.51:40490')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path='C:/Users/anil4/Desktop/kwork/job/parser_uber/chromedriver', options=chrome_options)  # desired_capabilities=capabilities options=chrome_options
driver.create_options()

def main():
    def normalize_data(text):
        return float(text.replace(' ', '').replace(',', '.'))
    time_start = time.perf_counter()
    # driver.get('http://ubertarif.ru/t/33sdw')
    search_price(driver)
    """print(driver.find_element(By.XPATH, '//a[@id="update"]'))
    time.sleep(10)
    while driver.find_element(By.XPATH, '//a[@id="update"]') == []:
        None
    driver.find_element(By.XPATH, '//a[@id="update"]').click()
    time.sleep(30)"""
    price = 'None'
    while re.search(r'\d', price[0]) is None:
        try:
            page = BeautifulSoup(driver.page_source, 'html.parser')
            price = page.find_all('ul', id='fares')[0].find_all('li')[0].text.replace(' ', '').replace('\n', '').split(
                'uberX:')[-1].replace('RUB', '').split('(')[0]
            time_price = datetime.strptime('%s-%s-%s %s:%s' % (
                datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                datetime.now().minute),
                                           '%Y-%m-%d %H:%M')
        except Exception as e:
            search_price(driver)
    print('%s : %s' % (time_price, price))

    driver.set_page_load_timeout(10)
    search_weather(driver)
    page_weather = BeautifulSoup(driver.page_source, 'html.parser')
    wheather = page_weather.find('div', class_='now-desc').text
    wind = [page_weather.find('div', class_='unit unit_wind_m_s').text.replace(
        page_weather.find('div', class_='item-measure').text, ''),
            page_weather.find('div', class_='item-measure').find_all('div')[0].text,
            page_weather.find('div', class_='item-measure').find_all('div')[-1].text]
    temperature = page_weather.find('span', class_='unit unit_temperature_c').text
    print('%s, %s м/с %s, %s' % (wheather, wind[0], wind[2], temperature))
    db_creater.insert_item(db_creater.create_id() ,time_price, normalize_data(price), wheather,
                      normalize_data(wind[0]), wind[2], normalize_data(temperature))  # время, цена, погода, ветер, температура


    while time.perf_counter() - time_start < 1 * 30:
        None

while True:
    db_creater.create_db()
    try:
        main()
    except:
        time.sleep(5)
        main()