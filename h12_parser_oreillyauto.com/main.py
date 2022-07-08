import create_db
import browser
import time
import sys

class Parser:
    def __init__(self, brow, proxy, page, make, year):
        self.proxy = proxy
        self.brow = brow
        self.page = page
        self.make = make
        self.year = year
        self.model = None
        self.models = None
        self.sub_model = None
        self.sub_models = None
        self.engine = None
        self.engines = None
        self.check = False
        try:
            self.last_item = [i for i in create_db.ckeck_last_car()]
        except:
            self.last_item = None

    def take_car(self):
        def take_buttons(len_selectors, selectors):
            text_selectors = [browser.text_selector(self.page, b) for b in selectors]
            while len_selectors == len([i for i in browser.find_selectors(self.page, 'li.ivs__option')]):
                time.sleep(1)
                print('pause')

            res_selectors = [i
                             for i
                             in browser.find_selectors(self.page, 'li.ivs__option')
                             if browser.text_selector(self.page, i) not in text_selectors]
            return res_selectors
        browser.goto(self.page, 'https://www.oreillyauto.com/')

        # Открытие выбора авто
        browser.wait_selector(self.page, 'button.header-icon-button')
        selector = browser.find_selectors(self.page, 'button.header-icon-button')[-1]
        browser.click_selector(self.page, selector)
        print('Открылось окно выбора машины')

        # Выбираю year и make
        selectors_year_make = []
        time_start = time.perf_counter()
        while year not in selectors_year_make and make not in selectors_year_make:
            selectors_year_make = [browser.text_selector(self.page, i).upper()
                                   for i
                                   in browser.find_selectors(self.page, 'li.ivs__option')]
            time.sleep(1)
            print('pause')
            if time.perf_counter() - time_start > 15:
                self.brow, self.page = browser.create_web(self.brow, self.page, self.proxy)
                return False
        selectors_year_make = browser.find_selectors(self.page, 'li.ivs__option')
        len_selectors = len(selectors_year_make)
        for sel in selectors_year_make:
            text_in_sel = browser.text_selector(self.page, sel).upper()
            if text_in_sel == '%s' % year:
                browser.click_selector(self.page, sel)
                print('year: ' + year)
                time.sleep(5)
                selectors = browser.find_selectors(self.page, 'li.ivs__option')
                selectors_names = [browser.text_selector(self.page, i) for i in selectors]
            if text_in_sel == ' %s ' % make:
                browser.click_selector(self.page, sel)
                print('make: ' + make)
                break
        time.sleep(5)
        selectors_model = take_buttons(len_selectors, selectors_year_make)
        len_selectors = len(selectors_model) + len_selectors
        selectors_model.extend(selectors_year_make)

        # Отсеивает уже сделаную модель
        model_names = []
        for model in selectors_model:
            model_name = browser.text_selector(self.page, model)
            if self.last_item is not None:
                if model_name == self.last_item[2]:
                    selectors_model = selectors_model[selectors_model.index(model):]
            model_names.append(model_name)
        if self.models is None:
            self.models = [i for i in model_names[:model_names.index(selectors_names[0])] if i not in selectors_names]
            if self.models == []:
                self.models = selectors_names[1:]
                selectors_names = [selectors_names[0]]
            selectors_model = [i for i in selectors_model if browser.text_selector(self.page, i) in self.models]


        self.model = browser.text_selector(self.page, selectors_model[0])
        print('model: ' + self.model)
        browser.click_selector(self.page, selectors_model[0])

        time.sleep(5)
        selectors_sub_models = take_buttons(len_selectors, selectors_model)
        len_selectors = len(selectors_sub_models) + len_selectors
        selectors_sub_models.extend(selectors_model)

        sub_model_names = []
        for sub_model in selectors_sub_models:
            sub_model_name = browser.text_selector(self.page, sub_model)
            if self.last_item is not None:
                if sub_model_name == self.last_item[3]:
                    selectors_sub_models = selectors_sub_models[selectors_sub_models.index(sub_model):]
            sub_model_names.append(sub_model_name)
        if self.sub_models is None:
            self.sub_models = [i for i in sub_model_names[:sub_model_names.index(self.model)] if i not in self.models and i not in selectors_names]
            if self.sub_models == []:
                self.sub_models = self.models[1:]
                self.models = [self.models[0]]
            selectors_sub_models = [i for i in selectors_sub_models if browser.text_selector(self.page, i) in self.sub_models]
        #try:
        #    if self.last_item[3] == 'None':
        #        selectors_sub_models = selectors_sub_models[:len(self.sub_models)]
        #except:
        #    None

        self.sub_model = browser.text_selector(self.page, selectors_sub_models[0])
        print('sub_model: ' + self.sub_model)
        browser.click_selector(self.page, selectors_sub_models[0])

        time.sleep(5)
        selectors_engine = take_buttons(len_selectors, selectors_sub_models)
        len_selectors = len(selectors_engine) + len_selectors
        selectors_engine.extend(selectors_sub_models)

        engine_names = []
        for engine in selectors_engine:
            engine_name = browser.text_selector(self.page, engine)
            if self.last_item is not None:
                if engine_name == self.last_item[4]:
                    selectors_engine = selectors_engine[selectors_engine.index(engine):]
            engine_names.append(engine_name)
        if self.engines is None:
            self.engines = [i for i in engine_names[:engine_names.index(self.sub_model)] if i not in self.sub_models and i not in self.models and i not in selectors_names]
            if self.engines == []:
                self.engines = self.sub_models[1:]
                self.sub_models = [self.sub_models[0]]
            selectors_engine = [i for i in selectors_engine if browser.text_selector(self.page, i) in self.engines]
        #try:
        #    if self.last_item[4] == 'None':
        #        selectors_engine = selectors_engine[:len(self.engines)]
        #except:
        #    None
        #for i in selectors_engine:
        #    print(browser.text_selector(self.page, i))
        self.engine = browser.text_selector(self.page, selectors_engine[0])
        print('engine: ' + self.engine)
        browser.click_selector(self.page, selectors_engine[0])
        time.sleep(1)
        browser.click_selector(self.page, browser.find_selector(self.page, 'span.button-submit__button-text'))
        return True

    def pars(self):
        def parse_categories(sub_category):
            if sub_category is None:
                return None
            hrefes = []
            for i in sub_category:
                href = browser.href_selector(self.page, i)
                if href is None:
                    return None
                hrefes.append(href)

            if hrefes == []:
                return None
            return hrefes

        def category_step(href_sub_category):
            browser.goto(self.page, href_sub_category)
            if browser.find_selector(self.page, '.featured-category-title.col-xs-12') == None:
                return True
            else:
                sub_sub_categories = browser.find_selectors(self.page, 'a.featured-category-link')
                href_sub_categories = parse_categories(sub_sub_categories)
                return href_sub_categories

        def parse_items(category_text, story):
            print(category_text)
            selector = browser.find_selectors(self.page, 'a.btn-link.btn--md')
            if selector is not None and selector != []:
                url = browser.href_selector(self.page, selector[-1])
            try:
                url, last_page = url.split('page=')
            except:
                last_page = 1
            for page in range(1, int(last_page) + 1):
                if page != 1:
                    browser.goto(self.page, url + 'page=%s' % str(page))
                items = browser.find_selectors(self.page, 'article.product.product--plp.product--interchange.js-product')

                for button in browser.find_selectors(self.page, 'button.toggle-expand.attribute-show-links.show-more'):
                    browser.click_selector(self.page, button)

                for item in items:
                    supplier_selector = browser.find_selector(item, 'dd.part-info__code.js-ga-product-line-code')
                    supplier_text = browser.text_selector(self.page, supplier_selector)
                    if supplier_text == '':
                        supplier_text = None

                    try:
                        location_text = browser.text_selector(self.page, browser.find_selector(browser.find_selector(item, 'div.attribute_wrap'), 'span'))
                    except:
                        location_text = 'None'

                    if location_text == 'Location:':
                        location_selector = browser.find_selector(browser.find_selector(item, 'div.attribute_wrap'), 'strong')
                        location_text = browser.text_selector(self.page, location_selector)
                    else:
                        location_text = 'None'

                    part_number_selector = browser.find_selector(item, 'dd.part-info__code.js-ga-product-line-number')
                    part_number_text = browser.text_selector(self.page, part_number_selector)
                    if part_number_text == '':
                        part_number_text = None

                    img_selector = browser.find_selector(item, 'img.product__image.lazy')
                    img_url = browser.src_selector(self.page, img_selector)
                    if img_url == '':
                        img_url = None

                    title_selector = browser.find_selector(item, 'h2.js-product-name.js-ga-product-name.product__name')
                    title_text = browser.text_selector(self.page, title_selector)
                    if title_text == '':
                        title_text = None

                    description_selector = browser.find_selector(item, 'div.attributes')
                    description_text = browser.text_selector(self.page, description_selector).replace('\n', '').replace('  ', '')
                    if description_text == '':
                        description_text = None

                    create_db.insert_item(create_db.create_id(), self.year, self.make, self.model, self.sub_model, self.engine,
                                          category_text, supplier_text, location_text, part_number_text, img_url, title_text, description_text, story)
                    # print(supplier_text, location_text, part_number_text, img_url, title_text, description_text, sep=' | ')

        def step(href_sub_category, story, last_story):
            hrefes = category_step(href_sub_category)
            if hrefes is True:
                category_selector = browser.find_selector(self.page, 'ul.site-breadcrumb_list.js-site-breadcrumb_list.orly-breadcrumb-list')
                category_text = browser.text_selector(self.page, category_selector)
                if self.last_item is not None and self.check is False:
                    if last_story:
                        if last_story[-1] == href_sub_category:
                            self.check = True
                            return parse_items(category_text.replace('  ', ' ').replace(' Home ', ''), story)
                else:
                    return parse_items(category_text.replace('  ', ' ').replace(' Home ', ''), story)
            else:
                if self.last_item is not None and last_story is not None:
                    hrefes = hrefes[hrefes.index(last_story[0]):]
                for href in hrefes:
                    story += ';' + href
                    if last_story is not None:
                        step(href, story, last_story[1:])
                    else:
                        step(href, story, None)

        href_sub_categories = None
        while href_sub_categories is None:
            sub_category = browser.find_selectors(self.page, 'a.nav_sub-link.orly-header-shop-item-sub')
            href_sub_categories = parse_categories(sub_category)

        if self.last_item is not None and self.check is False:
            self.last_item[-1] = [i for i in self.last_item[-1].split(';')]
            try:
                href_sub_categories = href_sub_categories[href_sub_categories.index(self.last_item[-1][0]):]
            except:
                None
        for href_sub_category in href_sub_categories:
            if self.last_item is not None and self.check is False:
                step(href_sub_category, href_sub_category, self.last_item[-1][1:])
            else:
                step(href_sub_category, href_sub_category, None)
        self.check = True

        self.last_item = [i for i in create_db.ckeck_last_car()]
        if self.engines.index(self.engine) == (len(self.engines) - 1):
            self.engines = None
            self.last_item[4] = 'None'
            print('Двигатели закончили')
            if self.sub_models.index(self.sub_model) == (len(self.sub_models) - 1):
                self.sub_models = None
                self.last_item[3] = 'None'
                print('Под модели закончили')
                if self.models.index(self.model) == (len(self.models) - 1):
                    print('Выгрузка закончена!!!')
                else:
                    self.last_item[2] = self.models[self.models.index(self.model) + 1]
                    print('Сменили модель')
            else:
                self.last_item[3] = self.sub_models[self.sub_models.index(self.sub_model) + 1]
                print('Сменили под модель')
        else:
            self.last_item[4] = self.engines[self.engines.index(self.engine) + 1]
            print('Сменили двигатель')
        """
        Сделать смену авто по engine, потом по sub_model и model через last_item и список наименований
        """
        self.brow, self.page = browser.create_web(self.brow, self.page, self.proxy)




        """
        -Переход по какатегориям (исключить 'We're sorry, no results were found'), 
        иногда попадается futered иногда нет
        
        -Проверить location
        """





if __name__ == '__main__':
    proxy = ''
    # proxy = '192.186.148.168:8800'
    brow, page = browser.create_web('', '', proxy)

    create_db.create_item_db()
    # make, year = 'FORD', '2017'
    make, year = sys.argv[-2].upper(), sys.argv[-1]

    main_parser = Parser(brow, proxy, page, make, year)
    while True:
        try:
            check_parse = main_parser.take_car()
            if check_parse:
                main_parser.pars()
        except Exception as e:
            print(e)
    time.sleep(10000)



