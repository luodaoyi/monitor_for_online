# -*- coding: utf-8 -*-
import re
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


prices = ['6.99', '16.99', '19.99']
check_interval = 60
keys = [
    '你的Server酱的key',
    '其他的Server酱的key',
]
timeout = 20
notified = {}
notice_times = 5
driver = None


def check_special_offer():
    try:
        if not driver:
            start_driver()
        driver.get('https://www.online.net/en/summer-2017/sales')
        sid = driver.find_elements_by_name('server_offer')[0]
        driver.execute_script("arguments[0].setAttribute('value','10010')", sid)
        sid.submit()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if tds and tds[-1].find('form'):
                tds_text = [td.text for td in tds]
                price = tds_text[-2].replace(' € pre-tax', '').strip()
                details = '\n\n'.join(tds_text[:-1])
                if price in prices:
                    if notified.get(price, 0) < notice_times:
                        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        text = '{}O有货啦'.format(price)
                        desp = details + '\n\n' + send_time
                        notified[price] = notified.get(price, 0) + 1
                        print('{}O有货了，第{}次通知'.format(price, notified[price]))
                        for key in keys:
                            send_message(key, text, desp)
                            time.sleep(1)
                    else:
                        print('{}O的相关信息超过最大通知次数，不再微信通知...'.format(price))
                else:
                    notified.setdefault(price, 0)
    except Exception as e:
        print(e)
        pass
            

def send_message(key, text, desp = ''):
    url = 'https://sc.ftqq.com/{}.send'.format(key)
    data = {
        'text': text,
        'desp': desp
    }
    r = requests.post(url, data = data, timeout = timeout)


def start_driver():
    global driver
    chromeOptions = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        'profile.managed_default_content_settings.javascript': 2
    }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options = chromeOptions)
    # service_args=[]
    # service_args.append('--load-images=no')  ##关闭图片加载
    # service_args.append('--disk-cache=yes')  ##开启缓存
    # service_args.append('--ignore-ssl-errors=true') ##忽略https错误
    # service_args.append('--ignore-ssl-errors=true')
    # service_args.append('--ssl-protocol=TLSv1')
    # cap = webdriver.DesiredCapabilities.PHANTOMJS
    # cap["phantomjs.page.settings.javascriptEnabled"] = False
    # driver = webdriver.PhantomJS(desired_capabilities = cap, service_args = service_args)
    driver.implicitly_wait(timeout)
    driver.set_page_load_timeout(timeout)




def main():
    while True:
        try:
            check_special_offer()
            print('{}秒后再次检查,当前时间: {}'.format(check_interval, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            time.sleep(check_interval)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    main()
