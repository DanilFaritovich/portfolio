#from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
#from fake_useragent import UserAgent
import time
from lxml import html
from itertools import chain
from oauth2client.service_account import ServiceAccountCredentials
import gspread



work_sheet_name = 'Парсер'
orders_list_name = 'Лист1'


time_start = time.perf_counter()
#prox = Proxy()
#prox.proxy_type = ProxyType.MANUAL
#prox.http_proxy = "203.30.190.166:80"
#prox.http_proxy = "socks5://94.45.188.161:45786:Selnilegalno95:Y5v0KjE"

#capabilities = webdriver.DesiredCapabilities.CHROME
#prox.add_to_capabilities(capabilities)

time_start = time.perf_counter()
#ua = UserAgent()
#userAgent = ua.chrome
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.headless = True
#s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
driver.create_options()

link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
my_creds = ServiceAccountCredentials.from_json_keyfile_name('test.json',
                                                                link)  # формируем данные для входа из нашего json файла
client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
sheet = client.open(work_sheet_name)  # открываем нужную на таблицу и лист
google_list = sheet.worksheet(orders_list_name)

def connect(url):
    driver.get(url)
    time.sleep(1)
    try:
        return [driver.find_elements(By.XPATH,'//select[@class="form-control ng-untouched ng-pristine ng-valid"]')[0], driver.find_elements(By.XPATH,'//select[@class="form-control ng-untouched ng-pristine ng-valid"]')[1]]
    except:
        driver.quit()
        time.sleep(3)
        connect(url)

select_element_0, select_element_1 = connect('https://cryptoxscanner.com/binance/live')
select_object = Select(select_element_1)
select_object.select_by_index(3)
select_object = Select(select_element_0)
select_object.select_by_index(2)
time.sleep(10)

tree = html.fromstring(driver.page_source)
data = [[[i.get('title')],[b.text.replace(',', '').replace('.', ',') for b in i.xpath('td[@class="ng-tns-c0-0 ng-star-inserted"]/span/span')[:9]]] for i in tree.xpath('//tr[@class="ng-tns-c0-0 ng-star-inserted"]')]
google_list.clear()
google_list.insert_rows([list(chain(*b)) for b in data], 2)

print(time.perf_counter() - time_start)
while True:
    try:
        time_start = time.perf_counter()
        #a = google_list.col_values(1)[1:]
        #for coin in tree.xpath('//tr[@class="ng-tns-c0-0 ng-star-inserted"]'):
        #    if coin.get('title') not in a:
        #        a.append(coin.get('title'))
        tree = html.fromstring(driver.page_source)
        #data = []
        """for i in tree.xpath('//tr[@class="ng-tns-c0-0 ng-star-inserted"]'):
            data_second = []
            for b in i.xpath('td[@class="ng-tns-c0-0 ng-star-inserted"]/span/span')[:9]:
                data_second.append(b.text[1:-1].replace(',', '').replace('.', ','))
            data += [i.get('title'), data_second]"""
        data = [[[i.get('title')], [b.text.replace(',', '').replace('.', ',') for b in
                                    i.xpath('td[@class="ng-tns-c0-0 ng-star-inserted"]/span/span')[:9]]] for i in
                tree.xpath('//tr[@class="ng-tns-c0-0 ng-star-inserted"]')]

        #data = [[i.get('title'), [b.text for b in i.xpath('td[@class="ng-tns-c0-0 ng-star-inserted"]/span/span')[:9]]] for i in tree.xpath('//tr[@class="ng-tns-c0-0 ng-star-inserted"]')]
        #data = [[[i], data[data.index(i)+1]] for i in a]
        #main_list = list(chain(*[list(chain(*b)) for b in data]))
        main_list = list(chain(*[list(chain(*b)) for b in data]))
        list_of_range = google_list.range('A2:J%s' % str(len(data)+1))
        for i, val in enumerate(main_list):
            if i%10 != 0:
                list_of_range[i].value = val
        google_list.update_cells(list_of_range)
        #google_list.insert_rows([list(chain(*b)) for b in data], 2)
        while time.perf_counter() - time_start < 15:
            None
        print(time.perf_counter() - time_start)
    except:
        driver.quit()
        time.sleep(5)
        connect('https://cryptoxscanner.com/binance/live')
