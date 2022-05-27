import time
import pickle
import sqlite3
import sys
import json

from bs4 import BeautifulSoup

from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio


def create_db():
    conn = sqlite3.connect('cars.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cars(
       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       year TEXT,
       make TEXT,
       model TEXT);
    """)
    conn.commit()
    conn = sqlite3.connect('items.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS items(
           id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           year TEXT NOT NULL,
           make TEXT NOT NULL,
           model TEXT NOT NULL,
           category TEXT NOT NULL,
           name TEXT NOT NULL,
           number TEXT NOT NULL,
           url TEXT NOT NULL,
           image_url TEXT NOT NULL,
           price TEXT NOT NULL);
        """)
    conn.commit()


async def create_web():
    start_parm = {
        'headless': False,
        'ignoreHTTPSErrors': True,

        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            #'--proxy-server=http://138.128.3.60:8800',
            '--disable-web-security',
            '--ignore-certificate-errors',
            '--ignore-certificate-errors-spki-list',
        ],
    }
    with open('cookies.json') as f:
        cookies = json.load(f)
    print(cookies)
    browser = await launch(start_parm)
    page = await browser.newPage()
    """for i in cookies:
        await page.setCookie(i)"""
    #await page.setUserAgent(
    #    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
    await page.setViewport(viewport={'width': 1920, 'height': 1280})
    # await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
    print('OK')
    await stealth(page)
    await page.goto('https://www.napaonline.com', timeout=120000)
    """cookies = await page.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)"""
    return [browser, page]


async def parse_cars(page, year, make):
    url = 'https://www.napaonline.com/en/c/replacement-parts/201056700'
    """cookies = await page.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)"""
    exit()
    conn = sqlite3.connect('cars.db')
    cur = conn.cursor()
    await page.goto(url, timeout=120000)
    js = """() =>{ 
        document.getElementsByClassName('geo-selected-vehicle add')[0].click()
        }
        """
    await page.waitForFunction('document.querySelector(".geo-selected-vehicle.add")', visible=True)
    await page.evaluate(js)

    js = """() =>{ 
            document.getElementById('vehicleYear-selector').getElementsByClassName('geo-option-name')[0].click()
            }
            """
    await page.waitForFunction('document.querySelector(".geo-selection-type.geo-vehicleyear.active")', visible=True)
    await page.evaluate(js)

    js = """() =>{ 
                var op = document.getElementsByClassName('geo-vehicle-option');
                for (var i = 0; i < op.length; i++) {
                  if (op[i].textContent == '%s') {
                    op[i].click();
                    break;
                  }
                }
                }
                """ % year
    await page.waitForFunction('document.querySelector(".geo-vehicle-option")', visible=True)
    await page.evaluate(js)

    js = """() =>{ 
                        document.getElementById('vehicleMake-selector').getElementsByClassName('geo-option-name')[0].click()
                        }
                        """
    await page.waitForFunction('document.querySelector(".geo-selection-type.geo-vehiclemake.active")', visible=True)
    await page.evaluate(js)
    js = """() =>{ 
                        var op = document.getElementsByClassName('geo-vehicle-option');
                        for (var i = 0; i < op.length; i++) {
                          if (op[i].textContent == '%s') {
                            op[i].click();
                            break;
                          }
                        }
                        }
                        """ % make
    await page.waitForFunction('document.querySelector(".geo-vehicle-option")', visible=True)
    await page.evaluate(js)

    js = """() =>{ 
        document.getElementById('vehicleModel-selector').getElementsByClassName('geo-option-name')[0].click()
        }
        """
    await page.waitForFunction('document.querySelector(".geo-selection-type.vehiclemodel.geo-vehiclemodel.active")', visible=True)
    await page.evaluate(js)
    page_pars = BeautifulSoup(await page.content(), 'html.parser')
    start = time.perf_counter()

    make_list = [(year, make, id.text)
                 for id
                 in page_pars.find_all('li', class_='geo-vehicle-option-block')]
    for make in make_list:
        if cur.execute('SELECT id FROM cars WHERE year = ? and make = ? and model = ?;', make).fetchone() is None:
            cur.execute('INSERT INTO cars(year, make, model) VALUES(?,?,?);', make)
    conn.commit()
    print('Обработка моделей: %s' % str(time.perf_counter() - start))


async def parse(browser, page, car):
    url = 'https://www.napaonline.com/en/c/replacement-parts/201056700'
    #await stealth(page)
    await page.goto(url, timeout=120000)
    try:
        js = """() =>{ 
                    document.getElementsByClassName('geo-selected-vehicle add')[0].click()
                    }
                    """
        time.sleep(1)
        await page.evaluate(js)
    except:
        js = """() =>{ 
                            document.getElementsByClassName('geo-selected-vehicle added')[0].click()
                            }
                            """
        time.sleep(1)
        await page.evaluate(js)
    js = """() =>{ 
                    document.getElementsByClassName('geo-vehicle-add-new')[0].click()
                    }
                    """
    time.sleep(1)
    await page.evaluate(js)
    js = """() =>{ 
                    document.getElementById('vehicleYear-selector').getElementsByClassName('geo-option-name')[0].click()
                    }
                    """
    time.sleep(1)
    await page.evaluate(js)
    js = """() =>{ 
                            var op = document.getElementsByClassName('geo-vehicle-option');
                            for (var i = 0; i < op.length; i++) {
                              if (op[i].textContent == '%s') {
                                op[i].click();
                                break;
                              }
                            }
                            }
                            """ % car[0]
    time.sleep(1)
    await page.evaluate(js)
    js = """() =>{ 
                            document.getElementById('vehicleMake-selector').getElementsByClassName('geo-option-name')[0].click()
                            }
                            """
    time.sleep(1)
    await page.evaluate(js)
    js = """() =>{ 
                                        document.getElementById('vehicleMake-selector').getElementsByClassName('geo-option-name')[0].click()
                                        }
                                        """
    time.sleep(1)
    await page.evaluate(js)
    js = """() =>{ 
                                        var op = document.getElementsByClassName('geo-vehicle-option');
                                        for (var i = 0; i < op.length; i++) {
                                          if (op[i].textContent == '%s') {
                                            op[i].click();
                                            break;
                                          }
                                        }
                                        }
                                        """ % car[1]
    time.sleep(1)
    await page.evaluate(js)

    js = """() =>{ 
                                        document.getElementById('vehicleModel-selector').getElementsByClassName('geo-option-name')[0].click()
                                        }
                                        """
    time.sleep(0.5)
    await page.evaluate(js)
    js = """() =>{ 
                                            var op = document.getElementsByClassName('geo-vehicle-option');
                                            for (var i = 0; i < op.length; i++) {
                                              if (op[i].textContent == '%s') {
                                                op[i].click();
                                                break;
                                              }
                                            }
                                            }
                                            """ % car[2]
    await page.evaluate(js)
    js = """() =>{ 
                    document.getElementsByClassName('geo-add-cancel-vehiclediv')[0].getElementsByTagName('button')[0].click()
                    }
                    """
    time.sleep(1)
    await page.evaluate(js)

    url = 'https://www.napaonline.com/en/c/replacement-parts/201056700'
    await page.goto(url, timeout=120000)
    page_content = BeautifulSoup(await page.content(), 'html.parser')
    categories_0 = [categore['href']
                  for categore
                  in page_content.find('div', class_='category-container geo-category-list').find_all('a')]
    for categore_0 in categories_0:
        await page.goto('https://www.napaonline.com' + categore_0, timeout=120000)
        page_content = BeautifulSoup(await page.content(), 'html.parser')
        categories_1 = [categore['href']
                      for categore
                      in page_content.find('div', class_='category-container geo-category-list').find_all('a')]
        for categore_1 in categories_1:
            await page.goto('https://www.napaonline.com' + categore_1, timeout=120000)
            page_content = BeautifulSoup(await page.content(), 'html.parser')
            categories_2 = [categore['href']
                            for categore
                            in page_content.find('div', class_='geo-parttype-list-container').find_all('a')]
            for categore_2 in categories_2:
                n = 1
                print(categore_2)
                while True:
                    try:
                        await page.goto('https://www.napaonline.com' + categore_2 + '?page=%s' % n, timeout=120000)
                    except:
                        input('Обновите vpn и нажмите enter')
                        await page.goto('https://www.napaonline.com' + categore_2 + '?page=%s' % n, timeout=120000)
                    fun = """() => {
                          return document.querySelector(".geo-pod-lists-wrapper");
                          }
                          """
                    #await page.waitFor('.geo-prod_pod_title')
                    time_start = time.perf_counter()
                    while True:
                        try:
                            page_content = BeautifulSoup(await page.content(), 'html.parser')
                            res = [[car[0],
                                    car[1],
                                    car[2],
                                    '/'.join([b.text for b in page_content.find('ol', class_='geo-breadcrumb').find_all('span')]),
                                    i.find('a', class_='geo-prod_pod_title').text,
                                    i.find('div', class_='geo-pod-part').text.replace('Part #: ', ''),
                                    'https://www.napaonline.com' + i.find('a', class_='geo-prod_pod_title')['href'],
                                    i.find('img')['src'],
                                    i.find('div', class_='geo-pod-price-cost').find('div').text.replace('$', '')]
                                    for i
                                    in page_content.find_all('div', class_='geo-pod-lists-wrapper')]
                            if res != []:
                                break
                            if time.perf_counter() - time_start > 10:
                                res = None
                                break
                            try:
                                if page_content.find('h2').text == 'You are being rate limited':
                                    await browser.close()
                                    start_parm = {
                                        # Начать хромированный путь
                                        # Закройте браузер без заголовка По умолчанию запускается без заголовка
                                        "headless": False,
                                        "ignoreHTTPSErrors": True,

                                        "args": [
                                            '--no-sandbox',
                                            '--disable-setuid-sandbox',
                                            # '--proxy-server=http://138.128.25.112:8800',# Отключить режим песочницы
                                        ],
                                    }
                                    browser = await launch(**start_parm)
                                    page = await browser.newPage()
                                    await stealth(page)
                                    # await page.setUserAgent(
                                    #    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
                                    await page.setViewport(viewport={'width': 1920, 'height': 1280})
                            except Exception as e:
                                print(e)
                            time.sleep(1)
                        except Exception as e:
                            # if 'No results were found for' in div[class='geo-search-results-container'].h3.text
                            if time.perf_counter() - time_start > 15:
                                await page.goto('https://www.napaonline.com' + categore_2 + '?page=%s' % n,
                                                timeout=120000)
                                time_start = time.perf_counter()
                            #print('pause')
                            time.sleep(3)
                    if res is None:
                        time.sleep(15)
                        break
                    #print(res)
                    conn_items = sqlite3.connect('items.db')
                    cur_items = conn_items.cursor()
                    for res_item in res:
                        check_try = cur_items.execute('select id from items where year = ? and make = ? and model = ? and category = ? and name = ? and number = ?', res_item[:6])
                        if check_try.fetchone() is None:
                            cur_items.execute('''INSERT or ignore INTO items(year, make, model, category, name, number, url, image_url, price) 
                            VALUES(?,?,?,?,?,?,?,?,?);''', res_item)
                    conn_items.commit()
                    n += 1
    return [browser, page]


if __name__ == '__main__':
    # driver, chrome_options = create_web()
    browser, page = asyncio.get_event_loop().run_until_complete(create_web())
    create_db_flag = True

    if create_db_flag == True:
        create_db()
    conn_cars = sqlite3.connect('cars.db')
    cur_cars = conn_cars.cursor()

    year, make = sys.argv[1:]
    print(year, make, sep=' ')
    if cur_cars.execute('SELECT id FROM cars WHERE year = ? and make = ?', (year, make)).fetchone() is None:
        asyncio.get_event_loop().run_until_complete(parse_cars(page, str(year), make))

    conn_items = sqlite3.connect('items.db')
    cur_items = conn_items.cursor()
    model = cur_items.execute('SELECT model FROM items WHERE year = ? and make = ? ORDER BY id DESC LIMIT 1', (year, make)).fetchone()
    print(model)
    exit()
    if model is None:
        for car in cur_cars.execute('SELECT id FROM cars WHERE year = ? and make = ? and ORDER BY id', (year, make)).fetchall():
            browser, page = asyncio.get_event_loop().run_until_complete(parse(browser, page, car))
    else:
        for car in cur_cars.execute('SELECT id FROM cars WHERE year = ? and make = ? and model => ? ORDER BY id', (year, make, model)).fetchall():
            browser, page = asyncio.get_event_loop().run_until_complete(parse(browser, page, car))