# coding:utf-8
import time
from datetime import datetime
import requests

def send_message(text, desp):
    key = 'xxxxxx'  # https://sc.ftqq.com 这里注册 然后去用微信扫描生成一个key就行了
    url = f"https://sc.ftqq.com/{key}.send"
    data = {
        'text': text,
        'desp': desp
    }
    requests.post(url, data=data, timeout=20)

def check_server(id):
    url = f'https://www.kimsufi.com/en/order/kimsufi.cgi?hard={id}'
    with requests.get(url) as resp:
        if resp.content.find('icon-availability'):
            return True
    return False

def main():
    if check_server('1804sk932'):
        desp = '''
        正常订单地址：https://www.kimsufi.com/en/order/kimsufi.cgi?hard=1804sk932 \n\n
        欧元配置页面地址：https://www.kimsufi.com/fr/commande/kimsufi.xml?reference=1804sk932 \n\n
        美元英文配置页面地址：https://www.kimsufi.com/us/en/order/kimsufi.xml?reference=1804sk932 \n\n
        美元法文配置页面地址：https://www.kimsufi.com/us/fr/commande/kimsufi.xml?reference=1804sk932 \n\n
        加元英文配置页面地址：https://www.kimsufi.com/ca/en/order/kimsufi.xml?reference=1804sk932 \n\n
        加元法文配置页面地址：https://www.kimsufi.com/ca/fr/commande/kimsufi.xml?reference=1804sk932
        '''
        send_message('KS-3C 特价有货',desp)
    if check_server('174sk94'):
        desp = '''
        https://www.kimsufi.com/en/order/kimsufi.cgi?hard=174sk94
        '''
        send_message('新版ks4a特价有货',desp)
    if check_server('174sk942'):
        desp = '''
        https://www.kimsufi.com/en/order/kimsufi.cgi?hard=174sk942
        '''
        send_message('新版ks4c特价有货',desp)

if __name__ == '__main__':
    main()