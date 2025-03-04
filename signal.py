import pandas as pd
import matplotlib.pyplot as plt

sentiment_data = pd.read_csv('market_sentiment.csv')
sentiment_data['Date'] = pd.to_datetime(sentiment_data['Date'])
sentiment_data.set_index('Date', inplace=True)

stock_data = pd.read_csv('stock_data.csv')
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

data = pd.merge(stock_data, sentiment_data, left_index=True, right_index=True, how='inner')

data['Price_Change'] = data['Close'].pct_change() * 100
data['Price_Change'].fillna(0, inplace=True)

data.fillna(method="bfill", inplace=True)

signals = []

for i in range(len(data)):
    signal = 0  # 0: 持有, 1: 买入, -1: 卖出

    if data['Sentiment'][i] >= 0.8:
        if data['Price_Change'][i] > 2:
            signal += 1

    signals.append(signal)

data['Signal'] = signals

print(data[['Close', 'SMA_50', 'SMA_200', 'Price_Change', 'Sentiment', 'Signal']].tail(10))

plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label="股票价格", color='black')
plt.plot(data['SMA_50'], label="50日SMA", color='blue')
plt.plot(data['SMA_200'], label="200日SMA", color='red')

buy_signals = data[data['Signal'] == 1]
plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label="买入信号")

plt.title(f"股票交易信号（涨幅>2% 且 情绪分析>80%）")
plt.legend(loc='best')
plt.show()