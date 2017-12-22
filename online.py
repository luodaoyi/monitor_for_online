# coding:utf-8
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

## 需要监控的价格
prices = ['6.99','16.99','19.99']
# 通知的server酱的key  https://sc.ftqq.com 这里注册
keys = [
    'xxxxxx',
]
# 批量订阅的发送key http://pushbear.ftqq.com/ 注册
send_key = 'xxxxxx'
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

# 发送消息通知
def send_message_all(key, text, desp=''):
    url = 'https://pushbear.ftqq.com/sub'
    data = {
        'sendkey':key,
        'text': text,
        'desp': desp
    }
    requests.post(url, data=data, timeout=timeout)

# 检查每条数据是不是有货
def check_server(tr):
    tds = tr.find_all('td')
    if tds and tds[-1].find('form'): #有form就是有货啊
        tds_text = [td.text for td in tds]
        
        name = tds_text[-8].strip()
        cpu = tds_text[-7].strip()
        mem_count = tds_text[-6].replace('Go','').strip() + "GB"
        disk = "SSD硬盘" if tds_text[-5].strip().find("SSD") else "普通硬盘"
        disk_count = tds_text[-5].strip()
        price = tds_text[-2].replace(' € pre-tax', '').strip()
        count = tds_text[-3].strip()

        if price in prices:
            if notified.get(price, 0) < notice_times:
                send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                text = f"{price}O_{disk}_库存{count}"
                details = f'配置项|数据 \n'
                details += f'----|---- \n'
                details += f'名称|{name} \n'
                details += f'CPU|{cpu} \n'
                details += f'内存|{mem_count} \n'
                details += f'硬盘|{disk_count} \n'
                details += f'价格|{price} € pre-tax \n'
                details += f'库存|{count} \n\n'
                
                desp ='## 配置信息: \n\n ' + details + '\n\n ##监控时间\n\n' + send_time + '\n\n ##购买地址\n\n ' + url + "\n\n"
                notified[price] = notified.get(price, 0) + 1
                #print(desp)
                print(f"{price}O有货了，第{notified[price]}次通知")

                # 发送单个人的
                for it_key in keys:
                    send_message(it_key, text, desp)
                # 发送push熊的
                send_message_all(send_key, text, desp)
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
