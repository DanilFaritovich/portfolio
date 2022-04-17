import re
import pandas as pd
date = {'01': 'Январь',
        '02': 'Февраль',
        '03': 'Март',
        '04': 'Апрель',
        '05': 'Май',
        '06': 'Июнь',
        '07': 'Июль',
        '08': 'Август',
        '09': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь'}

def check_numbers(text):
    try:
        re.findall(r'\d\d\d.{,11}\d', r'%s' % text)[0]
        if '50‑432‑7555' not in text:
            return text
        else:
            return ''
    except:
        return ''


def check_message(text):
    data = '%s %s 20%s' % (re.findall(r'\d\d.\d\d.\d\d', r'%s' % text)[0].split('.')[0],
                         date[re.findall(r'\d\d.\d\d.\d\d', r'%s' % text)[0].split('.')[1]],
                         re.findall(r'\d\d.\d\d.\d\d', r'%s' % text)[0].split('.')[2])
    number = re.findall(r'\d\d\d.{,11}\d', r'%s' % text)[0]
    print(r'%s' % re.findall(r'@.*: ', '%s' % text.replace('[', '@'))[0])
    print(text.replace(r'%s' % re.findall(r'@.*: ', '%s' % text.replace('[', '@'))[0], ''))
    name = text.replace('[', '@').replace(r'%s' % re.findall(r'@.*: ', '%s' % text.replace('[', '@'))[0], '').replace('%s' % number, '').replace('+', '')
    return [data, number, name]


if __name__ == '__main__':
    with open('_chat 2.txt', 'r', encoding='utf-8') as f:
        messages = f.read().replace('\n', '').replace('[', '@\n[')
        messages = messages.split('@')
    messages = [check_numbers(i).replace('Leonardo Visconti', '') for i in messages]
    print(messages)
    messages = [check_message(i) for i in messages[1:]
                    if i != '']
    new_messages = []
    for i in messages:
        if i not in new_messages:
            new_messages.append(i)
    #new_messages = [i for i in new_messages
    #                if i not in new_messages]

    with open('chat.txt', 'w', encoding='utf-8') as f:
        for i in new_messages:
            f.write('%s\n' % i[0])

    df = pd.DataFrame(new_messages, columns=['date', 'number', 'name'])
    writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Лист 1', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Лист 1']
    print(worksheet)
    worksheet.set_column('A:C', 20)
    writer.save()
