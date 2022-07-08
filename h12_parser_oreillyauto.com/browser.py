import time

from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio

def create_web(browser, page, proxy):
    print('proxy: %s' % proxy)
    async def event(browser, page, proxy):
        if browser != '':
            await page.close()
            try:
                await browser.close()
            except:
                None
            print('Браузер закрыт')
        start_parm = {
            'headless': False,
            'ignoreHTTPSErrors': True,

            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                f'--proxy-server={proxy}',
                '--disable-web-security',
                '--ignore-certificate-errors',
                '--ignore-certificate-errors-spki-list',
            ],
        }
        browser = await launch(**start_parm)
        page = await browser.newPage()
        #await page.setUserAgent(
        #    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
        await page.setViewport(viewport={'width': 1920, 'height': 1280})
        await stealth(page)
        await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
        return [browser, page]
    return asyncio.get_event_loop().run_until_complete(event(browser, page, proxy))

def goto(page, url):
    async def event(page, url):
        return await page.goto(url, timeout=120000)
    return asyncio.get_event_loop().run_until_complete(event(page, url))

def wait_selector(page, text):
    async def event(page, text):
        return await page.waitForSelector(text)
    return asyncio.get_event_loop().run_until_complete(event(page, text))

def find_selector(page, text):
    async def event(page, text):
        return await page.querySelector(text)
    return asyncio.get_event_loop().run_until_complete(event(page, text))

def find_selectors(page, text):
    async def event(page, text):
        try:
            return await page.querySelectorAll(text)
        except Exception as e:
            print(e)
            return None
    return asyncio.get_event_loop().run_until_complete(event(page, text))

def text_selector(page, sel):
    async def event(page, sel):
        try:
            return await page.evaluate('(element) => element.textContent', sel)
        except Exception as e:
            print(e)
    return asyncio.get_event_loop().run_until_complete(event(page, sel))

def href_selector(page, sel):
    async def event(page, sel):
        try:
            return await page.evaluate('(element) => element.href', sel)
        except Exception as e:
            print(e)
            return None
    return asyncio.get_event_loop().run_until_complete(event(page, sel))

def src_selector(page, sel):
    async def event(page, sel):
        try:
            return await page.evaluate('(element) => element.src', sel)
        except Exception as e:
            print(e)
            return None
    return asyncio.get_event_loop().run_until_complete(event(page, sel))

def click_selector(page, sel):
    async def event(page, sel):
        return await page.evaluate('(element) => element.click()', sel)
    return asyncio.get_event_loop().run_until_complete(event(page, sel))

def take_content(page, sel):
    async def event(page, sel):
        return await page.evaluate('(element) => element.click()', sel)
    return asyncio.get_event_loop().run_until_complete(event(page, sel))