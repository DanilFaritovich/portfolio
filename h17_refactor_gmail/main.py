import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import zipfile
import requests
with open('proxy.txt', 'r') as f:
    proxies = [i.replace('\n', '') for i in f.readlines()]
    print(proxies)
with open('emails.txt', 'r') as f:
    emails = [[i.replace('\n', '')] for i in f.readlines()]
    print(emails)
    for i, proxy in enumerate(proxies):
        emails[i].append(proxy)
n = 1
for email in emails[2:3]:
    print(email)
    PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = email[-1].split(':')
    mail, password, second_mail, second_password, serial_number = email[0].split(':')
    recovery_email = 'hasnogame231@gmail.com'
    work_time = 6

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    ua = UserAgent()
    userAgent = ua.chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(pluginfile)
    #chrome_options.add_experimental_option("excludeSwitches", ['load-extension', 'enable-automation'])
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.headless = False
    # https://accounts.google.com/signin/v2/challenge/pwd?flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward&TL=AM3QAYZH7j0iTzxhZJDMM6-4P1vZXOevF0zu-Qq8EOcrfiJaJ3sJxHRQN3Lolp76
    ads_power = requests.get(f'http://local.adspower.com:50325/api/v1/browser/start?serial_number={serial_number}').json()
    chrome_options.debugger_address = ads_power["data"]["ws"]["selenium"]
    driver = webdriver.Chrome(executable_path=ads_power["data"]["webdriver"], chrome_options=chrome_options)
    driver.create_options()
    driver.get('https://accounts.google.com/ServiceLogin')
    print(mail)
    time.sleep(work_time)

    if 'Вы не вошли в аккаунт' in driver.page_source:
        while True:
            try:
                driver.find_element(By.XPATH, '//div[@class="tgnCOd"]')
                break
            except:
                time.sleep(1)
        time.sleep(work_time)
        driver.execute_script("""
            document.getElementsByClassName('tgnCOd')[0].click();
            """)

        while True:
            try:
                driver.find_element(By.XPATH, '//div[@class="KTeGk"]').click()
                break
            except:
                time.sleep(1)
        #time.sleep(work_time)
        #driver.execute_script("""
        #    document.getElementsByClassName('KTeGk')[0].click();
        #    """)

        while True:
            try:
                driver.find_element(By.XPATH, '//div')
                break
            except:
                time.sleep(1)
        time.sleep(work_time)
        driver.execute_script("""
            document.getElementsByClassName('BHzsHc')[0].click();
            """)

    # Логинит почту
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
            driver.find_element(By.XPATH, '//div[@class="VfPpkd-RLmnJb"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    driver.execute_script("""
        document.getElementsByClassName('whsOnd zHQkBf')[0].value = '%s';
        document.getElementsByClassName('VfPpkd-RLmnJb')[0].click();
        """ % mail)

    # Логинит пароль
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    driver.execute_script("""
            document.getElementsByClassName('whsOnd zHQkBf')[0].value = '%s';
            document.getElementsByClassName('VfPpkd-RLmnJb')[0].click();
            """ % password)

    # Проверка почты
    time_start = time.perf_counter()
    check_second_email_flag = False
    while True:
        try:
            time.sleep(work_time)
            driver.find_element(By.XPATH, '//div[@class="vxx8jf"]')
            check_second_email_flag = True
            break
        except:
            if time.perf_counter() - time_start > 3:
                break
            time.sleep(1)

    # Логин второй почты
    if check_second_email_flag:
        driver.execute_script("""
            document.getElementsByClassName('vxx8jf')[2].click()
            """)
        while True:
            try:
                driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
                break
            except:
                time.sleep(1)
        time.sleep(work_time)
        driver.execute_script("""
            document.getElementsByClassName('whsOnd zHQkBf')[0].value = '%s';
            document.getElementsByClassName('VfPpkd-vQzf8d')[0].click();
            """ % second_mail)

    time.sleep(work_time)
    if 'Защитите свой аккаунт' in driver.page_source:
        driver.execute_script("""
                    document.getElementsByClassName('RveJvd snByac')[1].click();
                    """)
    if 'Настройте персонализацию, чтобы сделать работу с Google максимально удобной.' in driver.page_source:
        driver.execute_script("""
                    document.getElementsByClassName('VfPpkd-vQzf8d')[0].click();
                    """)

    # Переход в настройки
    while True:
        try:
            driver.find_element(By.XPATH, '//h1[@class="x7WrMb"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    driver.get('https://myaccount.google.com/u/1/security')

    # Смена пароля
    # Заходим в смену пароля
    while True:
        try:
            driver.find_element(By.XPATH, '//h3[@class="bJCr1d"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    for i in driver.find_elements(By.XPATH, '//h3[@class="bJCr1d"]'):
        if i.text == 'Password':
            i.click()
            break

    # Логинимся для смены пароля
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    driver.execute_script("""
        document.getElementsByClassName('whsOnd zHQkBf')[0].value = '%s';
        document.getElementsByClassName('VfPpkd-vQzf8d')[0].click();
        """ % password)

    # Меняем пароль
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@class="VfPpkd-fmcmS-wGMbrd uafD5"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    while True:
        try:
            driver.execute_script("""
                document.getElementsByTagName('input')[3].value = '%s';
                document.getElementsByTagName('input')[4].value = '%s';
                document.getElementsByClassName('VfPpkd-vQzf8d')[0].click();
                """ % (second_password, second_password))
            break
        except:
            time.sleep(1)

    # Переходим в смену email
    while True:
        try:
            driver.find_element(By.XPATH, '//div[@class="Dn5CSc"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    for i in driver.find_elements(By.XPATH, '//h3[@class="bJCr1d"]'):
        if i.text == 'Recovery email':
            i.click()
            break

    # Логинимся для смены почты
    while True:
        try:
            driver.find_element(By.XPATH, '//input[@class="whsOnd zHQkBf"]')
            break
        except:
            time.sleep(1)
    time.sleep(work_time)
    driver.execute_script("""
            document.getElementsByClassName('whsOnd zHQkBf')[0].value = '%s';
            document.getElementsByClassName('VfPpkd-vQzf8d')[0].click();
            """ % second_password)

    # Меняем почту
    while True:
        time.sleep(work_time)
        driver.execute_script("""
            document.getElementsByClassName('VfPpkd-fmcmS-wGMbrd CtvUB')[0].value = '%s';
            document.getElementsByClassName('VfPpkd-vQzf8d')[1].click();
            """ % recovery_email)
        try:
            driver.find_element(By.XPATH, '//h2[@class="VfPpkd-k2Wrsb"]')
            break
        except:
            time.sleep(1)

    # Вводим проверочный код
    confirm = False
    while True:
        code = input('Введите код из резервной почты: ').replace(' ', '')
        time.sleep(work_time)
        driver.execute_script("""
            document.getElementsByClassName('VfPpkd-fmcmS-wGMbrd CtvUB')[1].value = '%s';
            document.getElementsByClassName('VfPpkd-RLmnJb')[3].click();
            """ % code)
        time_start = time.perf_counter()
        while True:
            try:
                labels = len(driver.find_elements(By.XPATH, '//label'))
                print(labels)
                if labels == 2:
                    break
                elif labels == 0 or time.perf_counter() - time_start > 15:
                    confirm = True
                    break
            except:
                break
        time.sleep(work_time)
        if confirm:
            break
        try:
            if driver.find_elements(By.XPATH, '//p[@class="VfPpkd-fmcmS-yrriRe-W0vJo-fmcmS VfPpkd-fmcmS-yrriRe-W0vJo-fmcmS-OWXEXe-Rfh2Tc-EglORb"]')[-1].get_attribute('aria-hidden') == 'true':
                break
            driver.execute_script("""
                document.getElementsByClassName('qerXTe')[0].click();
                """)
        except:
            break
    print(f'{n}) Почта {second_mail} успешно изменена на {recovery_email}')
    print(f'{n}  Пароль {password} успешно изменён на {second_password}'.replace(f'{n}', ' ' * len(str(n))))
    n += 1
    requests.get(f'http://local.adspower.com:50325/api/v1/browser/stop?serial_number={serial_number}')
    driver.quit()