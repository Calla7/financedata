# -*- coding: utf-8 -*-
from binance.client import Client
import pandas as pd
import datetime


api_key = 'llkbObOMei39D8oAQ7YN0UbaZojbNVn8PpOzrFPcfqJBMMUcyEPCWD1YnToZRlux'
api_secret = 'pDLe9WG6mfA8H6MCsnjOPo2J3Jkn6gTzrEEqDhXZYP4dsrZmlxEZRPeB2SSDymVG'


client = Client(api_key, api_secret)

symbol = 'BTCUSDT'


def get_market_data(symbol):
    """获取市场交易数据并保存为一个CSV"""
    depth = client.get_order_book(symbol=symbol)

    ticker_24hr = client.get_ticker(symbol=symbol)

    current_price = client.get_symbol_ticker(symbol=symbol)

    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "24 hours ago UTC")

    klines_data = []
    for kline in klines:
        open_time = datetime.datetime.utcfromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')  # 转换时间戳
        klines_data.append([
            open_time,  # 开盘时间
            kline[1],   # 开盘价
            kline[2],   # 最高价
            kline[3],   # 最低价
            kline[4],   # 收盘价
            kline[5],   # 成交量
        ])

    klines_df = pd.DataFrame(klines_data, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume'
    ])

    asks_df = pd.DataFrame(depth['asks'], columns=['Ask Price', 'Ask Amount'])
    bids_df = pd.DataFrame(depth['bids'], columns=['Bid Price', 'Bid Amount'])

    all_data = pd.concat([
        klines_df.assign(Data_Type='Kline'),  # 给K线数据添加一个标识列
        asks_df.assign(Data_Type='Asks'),    # 给卖单深度数据添加标识列
        bids_df.assign(Data_Type='Bids')     # 给买单深度数据添加标识列
    ], axis=0, ignore_index=True)

    all_data['Current Price'] = current_price['price']
    all_data['24hr Change'] = ticker_24hr['priceChangePercent']

    all_data.to_csv(f'{symbol}_market_data.csv', index=False)

    print("所有数据已成功保存到 CSV 文件。")

get_market_data(symbol)
