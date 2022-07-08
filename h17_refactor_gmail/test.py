import imaplib
import email
from email import message
import base64
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('hasnogame231@gmail.com', 'sveuvctecgyklqwm')
mail.list()

mail.select("inbox")

result, data = mail.search(None, 'ALL')
ids = data[0]  # Получаем сроку номеров писем
id_list = ids.split()  # Разделяем ID писем
print(id_list)
messages = []
for latest_email_id in id_list:
    #latest_email_id = id_list[-14]  # Берем последний ID
    print(latest_email_id)

    result, data = mail.fetch(latest_email_id, "(RFC822)")  # Получаем тело письма (RFC822) для данного ID

    raw_email = data[0][1]  # Тело письма в необработанном виде
    email_message = raw_email.decode('utf-8')
    messages.append(email_message)
with open('out.txt', 'w', encoding='utf-8') as f:
    f.writelines(messages)
# включает в себя заголовки и альтернативные полезные нагрузки
print(email_message)