import time
import sqlite3
import sys

from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio


def create_db():
    conn = sqlite3.connect('items.db')
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                year TEXT,
                make TEXT,
                model TEXT,
                engine TEXT,
                part_type TEXT,
                supplier TEXT,
                location TEXT,
                part_number TEXT,
                image_url TEXT,
                comment TEXT,
                description TEXT);
                """)
    conn.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


async def create_web(proxy):
    start_parm = {
        'headless': False,
        'ignoreHTTPSErrors': True,

        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            f'--proxy-server={proxy}',
            #'--disable-web-security',
            #'--ignore-certificate-errors',
            #'--ignore-certificate-errors-spki-list',
        ],
    }
    browser = await launch(start_parm)
    page = await browser.newPage()
    #await page.setUserAgent(
    #    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
    await page.setViewport(viewport={'width': 1920, 'height': 1280})
    # await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
    await stealth(page)
    return [browser, page]


async def parse_data(make, year, page):
    conn = sqlite3.connect('items.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(f"""
                SELECT *
                FROM items
                WHERE year = '{year}' and make = '{make}'
                ORDER BY id DESC
                LIMIT 1
                """)
    last_item = cur.fetchone()
    url = 'https://showmetheparts.com/'
    try:
        await page.goto(url, timeout=120000, waitUntil='networkidle2')
    except:
        print('Не рабочий прокси!!!')
        exit()

    await page.waitForSelector('ul#combo-1060-picker-listEl')
    selector = await page.querySelectorAll('ul#combo-1060-picker-listEl')
    selectors = await selector[0].querySelectorAll('li')
    for sel in selectors:
        if await page.evaluate('(element) => element.textContent', sel) == year:
            print(await page.evaluate('(element) => element.textContent', sel))
            await sel.click()
            break

    await page.waitForSelector('ul#combo-1061-picker-listEl')
    selector = await page.querySelectorAll('ul#combo-1061-picker-listEl')
    selectors = await selector[0].querySelectorAll('li')
    for sel in selectors:
        if await page.evaluate('(element) => element.textContent', sel) == make:
            print(await page.evaluate('(element) => element.textContent', sel))
            await sel.click()
            break

    await page.waitForSelector('ul#combo-1062-picker-listEl')
    selector_model = await page.querySelectorAll('ul#combo-1062-picker-listEl')
    selectors_models = await selector_model[0].querySelectorAll('li')
    if last_item is not None:
        for model in selectors_models:
            if last_item['model'] == await page.evaluate('(element) => element.textContent', model):
                selectors_models = selectors_models[selectors_models.index(model):]
                break

    for model in selectors_models:
        model_text = await page.evaluate('(element) => element.textContent', model)
        print(model_text)
        await page.evaluate('(element) => element.click()', model)

        await page.waitForSelector('ul#combo-1063-picker-listEl')
        time.sleep(5)
        selector_part_type = await page.querySelectorAll('ul#combo-1063-picker-listEl')
        selectors_part_type = await selector_part_type[0].querySelectorAll('li')

        if last_item is not None:
            for part_type in selectors_part_type:
                if last_item['part_type'].upper() == await page.evaluate('(element) => element.textContent', part_type):
                    selectors_part_type = selectors_part_type[selectors_part_type.index(part_type):]
                    break
        for part_type in selectors_part_type:
            print(await page.evaluate('(element) => element.textContent', part_type))
            #if await page.evaluate('(element) => element.textContent', part_type) == 'ENGINE MOUNT':
            await page.evaluate('(element) => element.click()', part_type)
            if selectors_part_type.index(part_type) == 0:
                time.sleep(5)
            try:
                error = await page.waitForSelector('ul#combo-1064-picker-listEl', timeout=10000)
                #await page.waitForFunction('document.querySelector("#combo-1064-inputEl")', visible=True,
                #                           timeout=10000)
                selector_engine = await page.querySelectorAll('ul#combo-1064-picker-listEl')
                selectors_engine = await selector_engine[0].querySelectorAll('li')
            except:
                selectors_engine = [None]

            if last_item is not None:
                for engine in selectors_engine:
                    if engine is not None:
                        if last_item['engine'] == await page.evaluate('(element) => element.textContent', engine):
                            selectors_engine = selectors_engine[selectors_engine.index(engine):]
                            last_item = None
                            break
                    else:
                        last_item = None
                        break

            for engine in selectors_engine:
                if engine is not None:
                    engine_text = await page.evaluate('(element) => element.textContent', engine)
                    await page.evaluate('(element) => element.click()', engine)
                else:
                    element_engine = await page.querySelector('div#combo-1064-trigger-picker')
                    await page.evaluate('(element) => element.click()', element_engine)
                    engine_block = await page.querySelector('ul#combo-1064-picker-listEl')
                    engine_text = await engine_block.querySelector('li')
                    engine_text = await page.evaluate('(element) => element.textContent', engine_text)
                print(engine_text)

                time.sleep(3)
                try:
                    error = await page.waitForSelector('div.PartsViewListWrap', timeout=10000)
                except:
                    await page.waitForSelector('#button-1072-btnIconEl')
                    view = await page.querySelector('#button-1072-btnIconEl')
                    await page.evaluate('(element) => element.click()', view)
                    try:
                        error = await page.waitForSelector('div.PartsViewListWrap', timeout=10000)
                    except:
                        print('Нет элементов для выгрузки')
                        status = await page.querySelector('#button-1005-btnEl')
                        await page.evaluate('(element) => element.click()', status)
                        break
                items = await page.querySelectorAll('div.PartsViewListWrap')
                for item in items:
                    elements = await item.querySelector('.PartsViewListDataWrap1')
                    elements = await elements.querySelectorAll('div')

                    supplier = location = part_number = comment = description = ''

                    for element in elements:
                        if 'Supplier' in await page.evaluate('(element) => element.textContent', element):
                            supplier = await page.evaluate('(element) => element.textContent', element)
                            supplier = supplier.replace('Supplier: ', '')
                        elif 'Location' in await page.evaluate('(element) => element.textContent', element):
                            location = await page.evaluate('(element) => element.textContent', element)
                            location = location.replace('Location: ', '')
                        elif 'Part Number' in await page.evaluate('(element) => element.textContent', element):
                            part_number = await page.evaluate('(element) => element.textContent', element)
                            part_number = part_number.replace('Part Number: ', '')
                        elif 'Part Type' in await page.evaluate('(element) => element.textContent', element):
                            part_type = await page.evaluate('(element) => element.textContent', element)
                            part_type = part_type.replace('Part Type: ', '')
                        elif 'Comment' in await page.evaluate('(element) => element.textContent', element):
                            comment = await page.evaluate('(element) => element.textContent', element)
                            comment = comment.replace('Comment: ', '')
                    image_object = await item.querySelector('.PartsViewImage')
                    image_url = await page.evaluate('(element) => element.src', image_object)

                    description_element = await item.querySelector('.PartsViewListDataWrap2')
                    description_element = await description_element.querySelector('div')
                    if 'Application' in await page.evaluate('(element) => element.textContent', description_element):
                        description = await page.evaluate('(element) => element.textContent', description_element)
                        description = description.replace('Application: ', '')

                    check_try = cur.execute("""
                    select id 
                    from items 
                    where year = ? and make = ? and model = ? and engine = ?
                    and part_type = ? and supplier = ? and location = ? and part_number = ? and image_url = ?
                    and comment = ? and description = ?
                    """, (year, make, model_text, engine_text, part_type, supplier, location, part_number, image_url, comment, description))
                    check = check_try.fetchone()
                    if check is None:
                        cur.execute('''
                        INSERT INTO items(year, make, model, engine, 
                        part_type, supplier, location, part_number, image_url, comment, 
                        description) 
                        VALUES(?,?,?,?,?,?,?,?,?,?,?);
                        ''', (year, make, model_text, engine_text, part_type, supplier, location, part_number, image_url, comment, description))
                        print(year, make, model_text, engine_text, part_type, supplier, location, part_number,
                              image_url, comment, description, sep=' ')

                    conn.commit()

if __name__ == '__main__':
    proxy = '192.186.148.168:8800'
    # proxy = ''
    browser, page = asyncio.get_event_loop().run_until_complete(create_web(proxy))

    create_db()

    # make, year = ['FORD', '2017']
    make, year = sys.argv[-2].upper(), sys.argv[-1]
    asyncio.get_event_loop().run_until_complete(parse_data(make, year, page))