import requests
import time
from fake_useragent import UserAgent
import os
from requests.adapters import HTTPAdapter
print(os.path.abspath(os.curdir))
f_in = open("url_all.txt", "r", encoding="utf-8")  # Входные сайты
with open("out.txt", "w+", encoding="utf-8") as f_out:
    f_out.write('')
with open("error.log", "w+", encoding="utf-8") as f_error:
    f_error.write('')
#f_out = open("out.txt", "a", encoding="utf-8")
#f_error = open("error.log", "a", encoding="utf-8")
user = UserAgent().opera
start_time = time.perf_counter()
f_in = [i for i in f_in.readlines()]
print(len(f_in))
for url in f_in:
    ua = UserAgent()
    userAgent = ua.chrome
    try:
        with requests.Session() as session:
            page = session.get('%s' % url.replace('\n', '').replace('\ufeff', ''), timeout=(1, 1), headers={'User-Agent': userAgent}) #, proxies={'http': 'http://203.30.191.25:80'})
        print('Прогнал: %s' % url.replace('\n', ''))
        if page.status_code == 200:
            if 'Protected by AntiBot.Cloud' in page.text:
                with open("error.log", "a", encoding="utf-8") as f_error:
                    f_error.write(url)
            else:
                with open("out.txt", "a", encoding="utf-8") as f_out:
                    f_out.write(url)
        else:
            with open("error.log", "a", encoding="utf-8") as f_error:
                f_error.write(url)
    except requests.exceptions.ConnectionError:
        with open("error.log", "a", encoding="utf-8") as f_error:
            f_error.write(url)
    except requests.exceptions.ReadTimeout:
        with open("out.txt", "a", encoding="utf-8") as f_out:
            f_out.write(url)
    except Exception as e:
        with open("error.log", "a", encoding="utf-8") as f_error:
            f_error.write(url)
print(time.perf_counter() - start_time)
input()
#f_out.close()
#f_error.close()