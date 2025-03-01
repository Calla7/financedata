# -*- coding: utf-8 -*-
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


def forecast_bitcoin_price_from_csv(csv_file, steps=10):

    data = pd.read_csv(csv_file, parse_dates=['Open Time'], index_col='Open Time')
    close_price = data['Close']
    model = ARIMA(close_price, order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)

    return forecast, model_fit, data

def plot_forecast(data, forecast, ticker, steps=10):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label=f'{ticker} 实际收盘价')

    future_dates = pd.date_range(start=data.index[-1], periods=steps + 1, freq='H')[1:]
    plt.plot(future_dates, forecast, label=f'{ticker} 预测收盘价', color='red')

    plt.legend()
    plt.title(f'{ticker} 收盘价预测')
    plt.xlabel('时间')
    plt.ylabel('收盘价 (USDT)')
    plt.grid(True)
    plt.show()


csv_file = 'D:/pythonProject/financedata1/DataResource/BTCUSDT_market_data.csv'
forecast, model_fit, data = forecast_bitcoin_price_from_csv(csv_file, steps=10)

plot_forecast(data, forecast, 'BTCUSDT', steps=10)