
from logger import logger
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

import amazonBot


def launch():
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-xss-auditor")
    opt.add_argument("--disable-web-security")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument("--allow-running-insecure-content")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--remote-debugging-port=921")
    opt.add_argument("--disable-webgl")
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome('chromedriver', options=opt, desired_capabilities=d)
    # opt.add_argument("--user-data-dir=selenium") # added this option to use cookies, you may need to perform initial login within Selenium
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(5)
    logger.info('Started Chrome')
    return browser

if __name__ == '__main__':
    try:
        b = launch()
        b.get(amazonBot.ITEM_URL)
    except Exception as inst:
        logger.error('Failed to open browser: {}'.format(format(inst)))

    try:
        done = False
        while(not done):
            try:
                if amazonBot.purchase_item(b):
                    done = True
                    logger.info("Successfully purchased item")
            except Exception as e:
                logger.error('ERROR: {}'.format(e))
    finally:
        logger.info('Closing Chromium')
        try:
            b.close()
        except BaseException:
            pass
        logger.info('Closed Chromium')