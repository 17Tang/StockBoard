# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:50:27 2020

@author: yabitang

"""
import numpy as np
import requests
import pandas as pd
import datetime

#抓上市股票代號
res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y")
df = pd.read_html(res.text)[0]
df = df.drop([0,1,5,6,7,8,9],axis = 1)
#抓上櫃股票代號
res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y")
df_otc = pd.read_html(res.text)[0]
df_otc = df_otc.drop([0,1,5,6,7,8,9],axis = 1)
Stock_ID = df.append(df_otc)
#print(Stock_ID)

def transform_date(date):
    y, m, d = date.split('/')
    return str(int(y)+1911) + '/' + m + '/' + d

def transform_data(data):
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))  #把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(data[3].replace(',', ''))
    data[4] = float(data[4].replace(',', ''))
    data[5] = float(data[5].replace(',', ''))
    data[6] = float(data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data

def transform(data):
    return [transform_data(d) for d in data]

def get_stock_history(date,stock_no):
    qoutes = []
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' %(date, stock_no)
    r = requests.get(url)
    data = r.json()
    return transform(data['data'])

# get_stock_history(20200921,2330)
def get_stock_history_otc(stock_no):
    url = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d=109/09&stkno=%s' %(stock_no)
    r = requests.get(url)
    data = r.json()
    return transform(data['aaData'])

a = get_stock_history_otc(6125)
b = get_stock_history(20200921,2330)

print('%.2f'%round(100*a[len(a)-1][7]/a[len(a)-2][6],3))
print('%.2f'%round(100*b[len(b)-1][7]/b[len(b)-2][6],3))