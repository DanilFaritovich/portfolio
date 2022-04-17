import gspread
from oauth2client.service_account import ServiceAccountCredentials  # ипортируем ServiceAccountCredentials
import sqlite3, datetime
import time

first_list_name = 'Лист 3'
second_list_name = 'Лист 4'
third_list_name = 'Лист 5'
dictionary_list_name = 'Словарь'
orders_list_name = 'Заказы'
work_sheet_name = 'Копия Данные для когортного анализа'
top_list = 'ТОПы покупок'


def create_list(list_name):
    try:
        sheet.del_worksheet(sheet.worksheet('%s' % list_name))
        sheet.add_worksheet('%s' % list_name, list_in.row_count + 1 , list_in.col_count + 1)
    except:
        sheet.add_worksheet('%s' % list_name, list_in.row_count + 1 , list_in.col_count + 1)


def create_date(user_date):
    b_1, b_2 = user_date.split(' ')[0], user_date.split(' ')[-1]
    b_1 = b_1.split('.')
    b_1[0], b_1[-1] = b_1[-1], b_1[0]
    if user_date.split(' ')[0] != user_date.split(' ')[-1]:
        user_date = '%s %s' % ('-'.join(b_1), b_2)
    else:
        user_date = '-'.join(b_1)
    return user_date


def insert_users_confirms(product, n):
    if "практика" not in product[2].lower() and "продление" not in product[2].lower() and product[3] != 0:
        n += 1
        cur.execute("INSERT INTO users_confirm VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (
            product[0], product[1], n, product[2], product[3], product[4], product[5], product[6]))
        #print(cur.execute("select * from users_confirm where order_number > 1 and order_number is not '' ").fetchall())
        #print("data_order = %s, id_user = %s, order_number = %s product = %s" % (
        #product[0], product[-2], n, product[2]))
    else:
        cur.execute("INSERT INTO users_confirm VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (
            product[0], product[1], '', product[2], product[3], product[4], product[5], product[6]))
        #print("data_order = %s, id_user = %s, order_number = %s product = %s" % (
        #product[0], product[-2], '', product[2]))
    return n


def sqlite_lower(value_):
    return value_.lower()

class create_lists():
    def __init__(self):
        self.header_title = list_in.row_values(1)[:7]
        self.header_last_list = ['before_buy_sum', 'before_user_count', 'before_buy', 'product', 'after_buy',
                            'after_user_count', 'after_buy_sum']
        self.header_top = ['order_number', 'product_dictonary', 'count', 'Sum']
    def create_tables(self):
        print(tuple(self.header_title))
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
               %s DATE,
               %s DATE,
               %s TEXT,
               %s REAL,
               %s TEXT,
               %s INTEGER,
               %s INTEGER);
               """ % tuple(self.header_title))
        cur.execute("""CREATE TABLE IF NOT EXISTS users_confirm(
           %s DATE,
           %s DATE,
           order_number INTEGER,
           %s TEXT,
           %s REAL,
           %s TEXT,
           %s INTEGER,
           %s INTEGER);
           """ % tuple(self.header_title))
        cur.execute("""CREATE TABLE IF NOT EXISTS users_top_buys(
                   %s REAL,
                   %s INTEGER,
                   %s TEXT,
                   %s TEXT,
                   %s TEXT,
                   %s INTEGER,
                   %s REAL);
                   """ % tuple(self.header_last_list))
        cur.execute("""CREATE TABLE IF NOT EXISTS top_buys(
                           %s TEXT,
                           %s INTEGER,
                           %s REAL);
                           """ % tuple(self.header_top[1:]))
    def insert_values(self):
        # Проверяем валидность данных
        user_list = [i[:7] for i in list_in.get_all_values()[1:]]
        for i in user_list:
            i[0] = create_date(i[0])
            i[1] = create_date(i[1])
        cur.executemany("INSERT INTO users VALUES(?, ? ,? ,? ,? ,? ,?);", user_list)
    def active(self):
        time_start = time.perf_counter()
        count_user_buy = dict()
        for id_user in cur.execute("SELECT DISTINCT id_user FROM users order by id_user;").fetchall():
            if id_user[0] == '':
                con = "SELECT * FROM users where id_user = %s order by date_order;" % 'null'
            else:
                con = "SELECT * FROM users where id_user = %s order by date_order;" % id_user
            user_product = cur.execute(con).fetchall()
            n = 0
            for product in user_product:
                if '/' in product[2]:
                    try:
                        number_type = int(product[2][product[2].index('/') + 1])
                    except:
                        n = insert_users_confirms(product, n)
                else:
                    n = insert_users_confirms(product, n)
            try:
                count_user_buy[n] += 1
            except KeyError:
                count_user_buy[n] = 1
        return count_user_buy
    def insert_list(self):
        time_start = time.perf_counter()
        content_all = []
        list_out_3.insert_rows([[self.header_title[0], self.header_title[1], 'order_number', self.header_title[2], self.header_title[3],
                                 self.header_title[4], self.header_title[5], self.header_title[6]]], 1)
        content = [[i for i in b] for b in cur.execute("SELECT * FROM users_confirm order by id_user;").fetchall()]
        # cur.execute("SELECT * FROM users_confirm order by id_user;").fetchall()
        list_out_3.insert_rows(content, 2)
    def count_user(self, count_user_buy):
        count_user_buy_confirm = dict()
        try:
            del count_user_buy[0]
        except:
            None
        for i in sorted(count_user_buy.items(), key=lambda item: item[1], reverse=True):
            if i[-1] != 0:
                count_user_buy_confirm[i[0]] = i[-1]
            else:
                break
        return count_user_buy_confirm
    @property
    def sort_list(self):
        def chech_buy(buy, product, in_keys):
            if buy != []:
                for i in in_keys:
                    if i[0] in buy[0]:
                        buy[0] = i[0]
                        break
                try:
                    product[buy[0]][0] += 1
                    product[buy[0]][1] += buy[1]
                except:
                    product[buy[0]] = [1, buy[1]]
            return product


        def sum_list_fun(i, list):
            sum_list = [list[key][i][dict][1]
                           for key in list
                           for dict in list[key][i]]
            return [sum_list, len(sum_list)]


        def user_list_fun(i, list):
            user_list = [list[key][i][dict][0]
                           for key in list
                           for dict in list[key][i]]
            return [user_list, len(user_list)]


        def product_list_fun(n, list):
            product_list_none = [dict
                                        for key in list
                                        for dict in list[key][n]]
            product_list = []
            for i in product_list_none:
                if type(i) == int:
                    product_list.append('')
                else:
                    product_list.append(i)
            return [product_list, len(product_list)]


        conn.create_function("LOWER", 1, sqlite_lower)
        create_list(third_list_name)
        list_out_5 = sheet.worksheet(third_list_name)
        list_in_dict_key = sheet.worksheet(dictionary_list_name)

        in_keys = list_in_dict_key.get_all_values()[1:]

        all_buy_dict = dict()
        content, content_before, content_after, key_list = [], [], [], []
        for key in in_keys:
            after_product, before_product = dict(), dict()
            buy = cur.execute("SELECT id_user, order_number FROM users_confirm where order_number > 0 and order_number is not '' and LOWER(product) like '%?%';".replace('?', key[0].lower())).fetchall()
            for user in buy:
                after_buy, before_buy = [], []
                if cur.execute("SELECT product, sum_order FROM users_confirm where id_user = ? and order_number = ?;", (user[0], user[1] + 1)).fetchone() != None:
                    after_buy = [i for i in cur.execute("SELECT product, sum_order FROM users_confirm where id_user = ? and order_number = ?;", (user[0], user[1] + 1)).fetchone()]
                if cur.execute("SELECT product, sum_order FROM users_confirm where id_user = ? and order_number = ? ;", (user[0], user[1] - 1)).fetchone() != None:
                    before_buy = [i for i in cur.execute("SELECT product, sum_order FROM users_confirm where id_user = ? and order_number = ? ;", (user[0], user[1] - 1)).fetchone()]

                after_product = chech_buy(after_buy, after_product, in_keys)
                before_product = chech_buy(before_buy, before_product, in_keys)

            before_product_len = len(before_product)
            after_product_len = len(after_product)
            if before_product_len > after_product_len:
                for i in range(before_product_len - after_product_len): after_product[i] = ['', '']
            elif before_product_len < after_product_len:
                for i in range(after_product_len - before_product_len): before_product[i] = ['', '']


            if after_product != {} or before_product != {}: all_buy_dict[key[0]] = [before_product, after_product]
            for i in range(len(before_product)): key_list += key

        before_sum_list = sum_list_fun(0, all_buy_dict)
        after_sum_list = sum_list_fun(1, all_buy_dict)

        before_user_list = user_list_fun(0, all_buy_dict)
        after_user_list = user_list_fun(1, all_buy_dict)

        before_product_list = product_list_fun(0, all_buy_dict)
        after_product_list = product_list_fun(1, all_buy_dict)

        for i in range(max(before_sum_list[-1],before_user_list[-1],before_product_list[-1],len(key_list),after_product_list[-1],after_user_list[-1],after_sum_list[-1])):
            conn.execute("INSERT INTO users_top_buys VALUES(?, ? ,? ,? ,? ,? ,?);", (before_sum_list[0][i], before_user_list[0][i], before_product_list[0][i], key_list[i], after_product_list[0][i], after_user_list[0][i], after_sum_list[0][i]))
        sort_date = conn.execute("SELECT * FROM users_top_buys ORDER BY product, after_user_count DESC;").fetchall()
        list_out_5.insert_rows([self.header_last_list], 1)
        list_out_5.insert_rows(sort_date, 2)

    def create_top(self):
        create_list(top_list)
        list_out_6 = sheet.worksheet(top_list)
        #conn.executemany("INSERT INTO top_buys VALUES(? ,? ,?);", conn.execute("SELECT product, order_number, sum_order FROM users_confirm;"))
        list_in_dict_key = sheet.worksheet(dictionary_list_name)
        in_keys = list_in_dict_key.get_all_values()[1:]
        sort_date = []

        for i in range(1, conn.execute("SELECT order_number FROM users_confirm WHERE order_number != '' ORDER BY order_number DESC LIMIT 1;").fetchone()[0] + 1):
            count_dict, sum_dict = {}, {}
            for key in in_keys:
                user_sum = 0
                request = conn.execute("SELECT product, order_number, sum_order FROM users_confirm WHERE LOWER(product) like '%/%' and order_number = %s;".replace('/', key[0].lower()).replace('%s', str(i))).fetchall()
                count_dict[key[0]] = len(request)
                for n in request:
                    user_sum += n[-1]
                sum_dict[key[0]] = user_sum
            for b in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)[:5]:
                sort_date.append([i, b[0], count_dict[b[0]], sum_dict[b[0]]])

        list_out_6.insert_rows([self.header_top], 1)
        list_out_6.insert_rows(sort_date, 2)

if __name__ == "__main__":

    time_start = time.perf_counter()
    link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
    my_creds = ServiceAccountCredentials.from_json_keyfile_name('user.json',
                                                                link)  # формируем данные для входа из нашего json файла
    client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
    sheet = client.open(work_sheet_name)  # открываем нужную на таблицу и лист
    list_in = sheet.worksheet(orders_list_name)
    print('Открываем главную таблицу и лист: %s' % (time.perf_counter() - time_start))

    # Создаём листы
    time_start = time.perf_counter()
    list_count = [first_list_name, second_list_name]
    for list_name in list_count[:2]:
        create_list(list_name)
    list_out_3 = sheet.worksheet(first_list_name)
    list_out_4 = sheet.worksheet(second_list_name)
    print('Создание листов 3, 4: %s' % (time.perf_counter() - time_start))

    time_start = time.perf_counter()
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    create_lists().create_tables()
    create_lists().insert_values()
    count_user_buy = create_lists().active()
    print('Добавил таблицу с count: %s' % (time.perf_counter() - time_start))

    time_start = time.perf_counter()
    create_lists().insert_list()
    print('Добавил 3 лист: %s' % (time.perf_counter() - time_start))

    time_start = time.perf_counter()
    count_user_buy_confirm = create_lists().count_user(count_user_buy)
    # Выгрузка в таблицу 4
    list_out_4.insert_rows([["user_count", "buy_count"]], 1)
    content = [[count_user_buy_confirm[i], i] for i in count_user_buy_confirm]
    list_out_4.insert_rows(content, 2)
    print('Добавление 4 листа: %s' % (time.perf_counter() - time_start))

    # Покупки до и после
    time_start = time.perf_counter()
    create_lists().sort_list
    print('sort_list: %s' % (time.perf_counter() - time_start))

    time_start = time.perf_counter()
    create_lists().create_top()
    print('create_lists: %s' % (time.perf_counter() - time_start))