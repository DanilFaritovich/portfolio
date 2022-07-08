import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import sqlite3
import pandas as pd
from multiprocessing import Process
import pickle
import os
from distutils.dir_util import copy_tree

mail = 'anil2003@mail.ru'
password = 'Danchiktv321'
ua = UserAgent()
userAgent = ua.chrome


def data_connect():
    conn = sqlite3.connect('main_base.db')

    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS t_currency(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                url TEXT,
                sale_count TEXT,
                sale_price TEXT,
                buy_count TEXT,
                buy_price TEXT)
                """)
    conn.commit()
    return conn



def check_excel():
    conn = data_connect()
    cur = conn.cursor()
    while True:
        #print('excel')
        try:
            val = [[str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4])]
                   for i in pd.read_excel('values.xlsx').values.tolist()]
            res = cur.execute("""SELECT * FROM t_currency ORDER BY id""").fetchall()
            for i in res:
                if list(i[1:]) not in val:
                    cur.execute("DELETE FROM t_currency WHERE id = '%s'" % i[0])
            for i in val:
                res = cur.execute("""SELECT id FROM t_currency
                                     WHERE url = '%s' and 
                                     sale_count = '%s' and
                                     sale_price = '%s' and
                                     buy_count = '%s' and
                                     buy_price = '%s';
                                     """ % (i[0], i[1], i[2], i[3], i[4]))
                if res.fetchone() == None:
                    cur.execute("""INSERT INTO t_currency(url, sale_count, sale_price, buy_count, buy_price) 
                                VALUES('%s', '%s', '%s', '%s', '%s')
                                """ % (i[0], i[1], i[2], i[3], i[4]))
            conn.commit()
        except Exception as e:
            time.sleep(1)
            print("excel сохранён | %s" % e)


def create_web(id):
    print('driver_start')
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.headless = True
    chrome_options.add_argument('--allow-profiles-outside-user-dir')
    chrome_options.add_argument('--enable-profile-shortcut-manager')
    chrome_options.add_argument(r'user-data-dir=%s\profiles\%s' % (os.getcwd(), id))
    chrome_options.add_argument('--profile-directory=Profile')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    driver.create_options()
    time.sleep(6)
    print('driver')
    return driver



def auth(driver):
    driver.get('https://phemex.com/ru/login')
    if driver.current_url == 'https://phemex.com/ru/login':
        driver.find_element(By.XPATH, '//input[@placeholder="Email"]').send_keys(mail)
        driver.find_element(By.XPATH, '//input[@placeholder="Пароль"]').send_keys(password)
        driver.find_element(By.XPATH, '//button[@class="f14 home-login-confirm svelte-114j00f primary br8"]').click()
        code = input('Введите код с почты: ')
        driver.find_element(By.XPATH, '//input[@placeholder="Код для нового устройства"]').send_keys(code)
        driver.find_element(By.XPATH, '//button[@class="f14 mt32 wp100 svelte-114j00f primary br8"]').click()
        time.sleep(1)
        driver.quit()
    driver.quit()




def check_crypto(id):
    try:
        try:
            os.mkdir('%s/profiles/%s' % (os.getcwd(), id))
        except:
            None

        if os.listdir('%s/profiles/%s' % (os.getcwd(), id)) == []:
            copy_tree('profiles/0', '%s/profiles/%s' % (os.getcwd(), id))
        #os.popen('copy User profiles/id')
        driver = create_web(id)
        conn = data_connect()
        cur = conn.cursor()

        try:
            url, sale_count, sale_price, buy_count, buy_price = cur.execute(
                "SELECT * FROM t_currency WHERE id = '%s'" % id).fetchone()[1:]
        except Exception as e:
            print("disconnect: %s" % url)
            return None
        print(url, sale_count, sale_price, buy_count, buy_price)
        driver.get(url)
        driver.implicitly_wait(3)
        try:
            driver.find_element(By.XPATH, '//i[@class="iconfont cp T3"]').click()
        except:
            None
        driver.find_element(By.XPATH, '//span[@class="market f1 tc H-1034vai"]').click()
        driver.find_element(By.XPATH, '//span[@class="BLUE usn wsn cp"]').click()
        # driver.find_element(By.XPATH, '//span[@class="BLUE usn wsn cp"]').click()
        #driver.execute_script('''window.open("https://phemex.com/spot/trade/ETHUSDT","_blank").focus();''')
        while True:
            try:
                if float(driver.find_element(By.XPATH, '//div[@class="f20 cp"]').text) >= float(sale_price):
                    driver.find_elements(By.XPATH, '//div[@class="wrap df T4 f14 ovh cp H-1muzdph"]/span')[-1].click()
                    try:
                        driver.find_element(By.XPATH, '//input[@class="f1 fw2 tr T1 H-1tibjdl"]').send_keys(str(sale_count))
                    except:
                        driver.find_element(By.XPATH, '//input[@class="f1 fw2 tr T1 H-1tibjdl has-text"]').send_keys(
                            str(buy_count))
                    driver.find_element(By.XPATH, '//div[@class="wrap df aic jcc br4 lh40 cp H-48siq7 btn-sell"]').click()
                    return None
                if float(driver.find_element(By.XPATH, '//div[@class="f20 cp"]').text) <= float(buy_price):
                    driver.find_elements(By.XPATH, '//div[@class="wrap df T4 f14 ovh cp H-1muzdph"]/span')[0].click()
                    try:
                        driver.find_element(By.XPATH, '//input[@class="f1 fw2 tr T1 H-1tibjdl"]').send_keys(str(buy_count))
                    except:
                        driver.find_element(By.XPATH, '//input[@class="f1 fw2 tr T1 H-1tibjdl has-text"]').send_keys(
                            str(sale_count))
                    driver.find_element(By.XPATH, '//div[@class="wrap df aic jcc br4 lh40 cp H-48siq7 btn-buy"]').click()
            except Exception as e:
                print('Остановлено: %s | error: %s' % (url, e))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        os.mkdir('%s/profiles/%s' % (os.getcwd(), 0))
    except:
        None
    driver = create_web(0)
    auth(driver)
    conn = data_connect()
    cur = conn.cursor()
    val = cur.execute("""SELECT id FROM t_currency ORDER BY id""").fetchall()
    print(val)
    #check_excel.remote()
    #check_crypto.remote(conn, val.fetchone()[0])
    #active_objects = ray.get([check_excel.remote(),
                      #auth.remote(drivers[0]),
                      #check_crypto.remote(conn, val.fetchone()[0])])
    #check_crypto(driver, conn, val.fetchone()[0])
    p1 = Process(target=check_excel)
    p1.start()
    process = [Process(target=check_crypto, args=(i[0],)) for i in val]
    print(process)
    for i in process:
        time.sleep(1)
        i.start()
    time.sleep(1000000)
