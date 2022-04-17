#!/usr/bin/env python
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
import time
import os
import re
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
import numpy as np


key_addr = 'Кварталы 1,2.txt'  # Название файла с ключами
res = 'res.xlsx'  # Имя excel файла
sheet = 'Search Result'  # Имя листа



prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "185.221.160.176:80"
capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

ua = UserAgent()
userAgent = ua.chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.headless = True
s = Service(ChromeDriverManager().install())
driver_new = webdriver.Chrome(service=s, chrome_options=chrome_options, desired_capabilities=capabilities)
driver_new.create_options()
driver_old = webdriver.Chrome(service=s, chrome_options=chrome_options, desired_capabilities=capabilities)
driver_old.create_options()
driver_old.get('https://old.bankrot.fedresurs.ru/Messages.aspx')
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

class Main:
    def start_program(self, file):
        def split_key(key):
            key = re.search(r'\d*:\d*:\d*', key)
            if key is not None:
                key = key.group()
            return key

        def atp(text):
            text = re.search(r'www.{,50}ru', text)
            if text is not None:
                text = text.group()
            return text

        def create_link_new(url, case):
            start_time = time.perf_counter()
            driver_new.stop_client()
            driver_new.get(url)
            time.sleep(1)
            print(time.perf_counter() - start_time)
            return driver_new.find_element(by=By.XPATH, value='//a[text()=" %s "]' % case).get_attribute('href')

        def create_link_old(driver, id):
            start_time = time.perf_counter()
            driver.execute_script('''
            document.getElementById("ctl00_cphBody_cldrBeginDate_tbSelectedDate").value =
                           document.getElementById("ctl00_cphBody_cldrBeginDate_tbSelectedDateValue").value = "";
            document.getElementById("ctl00_cphBody_tbMessageNumber").value = "%s";
            $('#ctl00_cphBody_ibMessagesSearch').click();
            ''' % id)
            time.sleep(1)
            print(time.perf_counter() - start_time)
            return driver.find_element(by=By.XPATH, value='//table[@class="bank"]//a').get_attribute('href')


        print(file)
        tree = (ET.parse('xml_files/%s' % file))
        root = tree.getroot()
        service = '{https://services.fedresurs.ru/BiddingService2}'
        soap_env = '{http://schemas.xmlsoap.org/soap/envelope/}'
        link_new_site = 'https://fedresurs.ru/search/bidding?searchString=%s&limit=15&tradeType=Все&lots=%7B%22lotStartPrice%22:null,%22lotFinishPrice%22:null%7D'
        """for TradePlace in root.findall('TradePlace'):
            for TradeList in TradePlace.findall('TradeList'):
                for Trade in TradeList.findall('Trade'):
                    ID_EXTERNAL = Trade.get('ID_EXTERNAL')
                    for Message in Trade.findall('Message'):
                        for Envelope in Message.findall('%sEnvelope' % soap_env):
                            for Body in Envelope.findall('%sBody'%soap_env):
                                for SetBiddingInvitation in Body.findall('%sSetBiddingInvitation'%service):
                                    for BiddingInvitation in SetBiddingInvitation.findall('%sBiddingInvitation'%service):
                                        for key in BiddingInvitation.iter('%sTradeObjectHtml' % service):
                                            print(':'.join(split_key(key.text).split(':')[:3]))"""
        keys = [i.replace(' ', '').replace('\n', '') for i in open('%s' % key_addr, 'r', encoding='utf-8').readlines()]
        list_of_trade = [[split_key(key.text), INN.get('INN'), IDEFRSB.text, Trade.get('ID_EXTERNAL'), create_link_new(new_link, Trade.get('ID_EXTERNAL')), create_link_old(driver_old, IDEFRSB.text), CaseNumber.get('CaseNumber') , 'xml_files/%s' % file, atp(ATP.text)]
                          for TradePlace in root.findall('TradePlace')
                          for TradeList in TradePlace.findall('TradeList')
                          for Trade in TradeList.findall('Trade')
                          for Message in Trade.findall('Message')
                          for Envelope in Message.findall('%sEnvelope' % soap_env)
                          for Body in Envelope.findall('%sBody' % soap_env)
                          for SetBiddingInvitation in Body.findall('%sSetBiddingInvitation' % service)
                          for BiddingInvitation in SetBiddingInvitation.findall('%sBiddingInvitation' % service)
                          for IDEFRSB in BiddingInvitation.iter('%sIDEFRSB' % service)
                          for INN in BiddingInvitation.iter('%sDebtorPerson' % service)
                          for CaseNumber in BiddingInvitation.iter('%sLegalCase' % service)
                          for key in BiddingInvitation.iter('%sTradeObjectHtml' % service)
                          for ATP in BiddingInvitation.iter('%sRules' % service)
                          for new_link in [link_new_site.replace('%s', Trade.get('ID_EXTERNAL'))]
                          if split_key(key.text) in keys]
        return list_of_trade


if __name__ == '__main__':
    start_time = time.perf_counter()
    all_data = []
    for file in os.listdir('xml_files'):
        all_data += Main().start_program(file)
    df = pd.DataFrame([i for i in all_data], columns=['Кадастровый номер ', 'ИНН банкрота', 'IDEFRSB', 'ID_EXTERNAL', 'Ссылка в ЕФРСБ (новая версия)', 'Ссылка в ЕФРСБ (старая версия)', '№ дела в картотеке арбитражных дел (CaseNumber)', 'Путь к файлу', 'ЭТП'])
    writer = pd.ExcelWriter(res, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet, index=False)
    worksheet = writer.sheets[sheet]
    worksheet.set_column('A:G', 25)
    writer.save()
    print('Парс файла xml: %s' % (time.perf_counter() - start_time))