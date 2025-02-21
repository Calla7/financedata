# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import os


stock_symbols = ['AAPL', 'GOOG', 'TSLA', '0700.HK', 'BABA', 'JD']
stock_names = ['Apple', 'Google', 'Tesla', 'Tencent', 'Alibaba', 'JD.com']


def get_stock_data(symbol):
    # 下载历史数据，指定时间范围为过去1个月，日线数据
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period="1mo", interval="1d")

    return stock_data


def save_to_csv(data, filename='stock_data.csv'):
    if os.path.exists(filename):
        data.to_csv(filename, mode='a', header=False, index=True)
    else:
        data.to_csv(filename, mode='w', header=True, index=True)

for symbol, name in zip(stock_symbols, stock_names):
    print(f"获取 {name} ({symbol}) 股票数据...")

    stock_data = get_stock_data(symbol)

    if stock_data.empty:
        print(f"警告: {symbol} ({name}) 没有数据或获取失败！")
    else:
        stock_data['Stock Name'] = name

        print(f"获取的 {name} ({symbol}) 股票数据：")
        print(stock_data)

        save_to_csv(stock_data)

    time.sleep(1)

print("所有数据已成功保存到 CSV 文件。")