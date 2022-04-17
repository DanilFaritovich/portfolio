from bs4 import BeautifulSoup
from lxml import html
import os
import re
import pandas as pd
import numpy as np


def check_number(text):
    try:
        number = re.findall(r'\d.{,14}\d', r'%s' % text)[0].replace(' ', '').replace('-', '')
        if ':' not in number:
            return number
    except:
        None

def user_contact(user, index):
    print('Сделал: %s' % index)
    with open(user, 'r', encoding='utf-8') as f:
        content = f.read()
        root = html.fromstring(content)
        #print(root.xpath('//div[@class="_3-95 _a6-g"]/div[@class="_2ph_ _a6-p"]/div/div'))
        mess = [i for i in root.xpath('//div[@class="_2ph_ _a6-p"]/div/div')]
        for message in mess:
            if message.text is not None:
                number = check_number(message.text)
                if number is not None:
                    index_message = mess.index(message) // 5
                    return [root.xpath('//div[@class="_a70e"]')[0].text, number, root.xpath('//div[@class="_a72d"]')[index_message].text]
                print(message.text)


messages = [i for i in os.listdir('messages/inbox')]
print('Всего: %s' % len(messages))
users = [user_contact('messages/inbox/%s/message_1.html' % user, messages.index(user))
         for user in messages]
users = [i for i in users
         if i is not None]


df = pd.DataFrame(users,
                  columns=['name', 'number', 'date'])
writer = pd.ExcelWriter('users.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Лист 1', index=False)
writer.save()