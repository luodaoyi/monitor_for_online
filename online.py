# coding:utf-8
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

## 需要监控的价格
prices = ['6.99','16.99', '19.99','15.99'] #15.99不是特价款 
# 通知的server酱的key  https://sc.ftqq.com 这里注册 然后去用微信扫描生成一个key就行了
keys = [
    'xxxxxxx',
]
# 检查间隔
check_interval = 60
# 服务器列表订购列表
url = "https://console.online.net/en/order/server"
notified = {}
## 通知次数
notice_times = 50
timeout = 20

# 获得购买页面
def get_page():
    with requests.get(url) as resp:
        return resp.content
# 发送消息通知
def send_message(key, text, desp=''):
    url = f"https://sc.ftqq.com/{key}.send"
    data = {
        'text': text,
        'desp': desp
    }
    requests.post(url, data=data, timeout=timeout)
# 检查每条数据是不是有货
def check_server(tr):
    tds = tr.find_all('td')
    if tds and tds[-1].find('form'): #有form就是有货啊
        tds_text = [td.text for td in tds]
        price = tds_text[-2].replace(' € pre-tax', '').strip()
        details = '\n\n'.join(tds_text[:-1]) 
        if price in prices:
            if notified.get(price, 0) < notice_times:
                send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                text = f"{price}O有货啦"
                desp = details + '\n\n 监控时间:   ' + send_time + '\n\n 购买地址:   ' + url
                notified[price] = notified.get(price, 0) + 1
                print(f"{price}O有货了，第{notified[price]}次通知")
                for key in keys:
                    send_message(key, text, desp)
                    time.sleep(1)
            else:
                print(f'{price}O的相关信息超过最大通知次数，不再微信通知...')
        else:
            notified.setdefault(price, 0)
# 跑脚本
def run():
    content = get_page()
    if not content:
        print('没有返回任何内容')
        return
    soup = BeautifulSoup(content, 'html.parser')
    trs = soup.find_all('tr')
    for tr in trs:
        check_server(tr)


def main():
    while True:
        try:
            run()
            print(
                f"{check_interval}秒后再次检查,当前时间: { datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(check_interval)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    main()