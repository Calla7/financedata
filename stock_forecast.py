import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def fetch_stock_data_from_csv(file_path, ticker):
    stock_data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    stock_data = stock_data[stock_data['Stock Name'] == ticker]

    stock_data = stock_data.sort_index()

    return stock_data

def time_series_forecast(data):
    close_price = data['Close']

    model = ARIMA(close_price, order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=10)
    return forecast

def plot_forecast(data, forecast, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label=f'{ticker}历史数据')

    forecast_index = pd.date_range(data.index[-1], periods=11, freq='D')[1:]

    plt.plot(forecast_index, forecast, label=f'{ticker}预测结果', color='red')
    plt.legend()
    plt.title(f"{ticker}预测")
    plt.xlabel('日期')
    plt.ylabel('收盘价')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

file_path = 'D:/pythonProject/financedata1/DataResource/stock_data.csv'

stock_data = pd.read_csv(file_path, parse_dates=['Date'])

unique_stocks = stock_data['Stock Name'].unique()

for ticker in unique_stocks:
    print(f"开始预测 {ticker} 股票数据...")

    stock_data_filtered = fetch_stock_data_from_csv(file_path, ticker)

    if stock_data_filtered.empty:
        print(f"{ticker} 的数据为空，跳过预测。")
        continue

    forecast = time_series_forecast(stock_data_filtered)

    print(f"{ticker} 股票未来10天预测:", forecast)

    plot_forecast(stock_data_filtered, forecast, ticker)