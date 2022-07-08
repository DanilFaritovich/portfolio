import time

import browser
import create_db

pers_class = 'Арбалестчик'

if __name__ == '__main__':
    create_db.create_item_db()
    with open('Духи.txt', 'r', encoding='utf-8') as f:
        spirits = [i.replace('\n', '') for i in f.readlines()]

    brow, page = browser.create_web('', '')
    browser.goto(page, 'https://www.xdraco.com/nft/list')
    print('goto')

    browser.wait_selector(page, 'button.btn-open-list.btn-language')
    selector = browser.find_selector(page, 'button.btn-open-list.btn-language')
    browser.click_selector(page, selector)

    selectors = browser.find_selectors(page, '.v-list-item.v-list-item--link.theme--light')
    selector = selectors[19]
    print(browser.text_selector(page, selector))
    browser.click_selector(page, selector)

    browser.wait_selector(page, 'div.v-select__selections')
    selectors = browser.find_selectors(page, 'div.v-select__selections')
    selector_1, selector_2 = selectors
    browser.click_selector(page, selector_1)

    browser.wait_selector(page, 'div.v-list-item__title')
    selectors = browser.find_selectors(page, 'div.v-list-item__title')
    for selector in selectors:
        if browser.text_selector(page, selector) == pers_class:
            browser.click_selector(page, selector)
            print(browser.text_selector(page, selector))
            break

    browser.click_selector(page, selector_2)
    browser.wait_selector(page, 'div.v-list-item__title')
    selectors = browser.find_selectors(page, 'div.v-list-item__title')
    for selector in selectors:
        if browser.text_selector(page, selector) == 'Цена: Самая низкая':
            browser.click_selector(page, selector)
            print(browser.text_selector(page, selector))
            break


    while True:
        check = browser.wait_selector(page, 'button.btn-viewmore')
        if check is None:
            break
        selector = browser.find_selector(page, 'button.btn-viewmore')
        if selector is None:
            break
        browser.click_selector(page, selector)
        item_list = browser.find_selectors(page, 'ul.list-item')[-1]
        if len(browser.find_selectors(item_list, 'a.link')) > 20:
           break
        print(len(browser.find_selectors(item_list, 'a.link')))

    browser.wait_selector(page, 'ul.list-item')
    item_list = browser.find_selectors(page, 'ul.list-item')[-1]
    last_items = [browser.href_selector(page, i)
             for i
             in browser.find_selectors(item_list, 'a.link')]
    items = []
    for item in last_items:
        if item not in items:
            items.append(item)
    items = ['https://www.xdraco.com/nft/trade/422626']
    for item in items:
        browser.goto(page, item)
        browser.wait_selector(page, 'div.v-slide-group__content.v-tabs-bar__content')
        main_selector = browser.find_selector(page, 'div.v-slide-group__content.v-tabs-bar__content')
        selector = browser.find_selectors(main_selector, 'div')[-1]
        text = browser.text_selector(page, selector)
        time_start = time.perf_counter()
        while text != 'Доступные духи':
            text = browser.text_selector(page, selector)
            main_selector = browser.find_selector(page, 'div.v-slide-group__content.v-tabs-bar__content')
            selector = browser.find_selectors(main_selector, 'div')[-1]
            if time.perf_counter() - time_start > 15:
                break
        browser.click_selector(page, selector)
        """while len(selectors) < 7:
            time.sleep(1)
            selectors = browser.find_selectors(page, '.tab-spirit-item.v-tab')
            print(len(selectors))
        selector = selectors[5]
        browser.click_selector(page, selector)"""

        browser.wait_selector(page, 'div.v-window-item.wrap-item-square')
        selector = browser.find_selector(page, 'div.v-window-item.wrap-item-square')
        # browser.wait_selector(selector, 'img')
        selectors = browser.find_selectors(selector, 'img')
        item_names = [browser.alt_selector(page, i)
                      for i
                      in selectors]
        if spirits[0] in item_names \
           and spirits[1] in item_names \
           and spirits[2] in item_names \
           and spirits[3] in item_names \
           and spirits[4] in item_names:
            name = browser.find_selector(page, 'h3.item-title')
            name = browser.text_selector(page, name)

            price = browser.find_selector(page, 'strong.ico-wemixcredit.ico-ss.add-inside')
            price = browser.text_selector(page, price)

            lvl = browser.find_selector(page, 'li.level')
            lvl = browser.find_selector(lvl, 'strong')
            lvl = browser.text_selector(page, lvl)
            print('Есть: %s' % item)
            print(name)
            print(price)
            print(lvl)
            id = create_db.create_id()
            print(id)
            create_db.insert_item(id, item, name, price, lvl)
        else:
            print('Нет: %s' % item)

    time.sleep(10000)