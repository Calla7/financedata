import pandas as pd

sentiment_data = pd.read_csv('D:/pythonProject/financedata1/SentimentAnalyse/sentiment_analysis_results.csv')
trading_data = pd.read_csv('D:/pythonProject/financedata1/DataResource/BTCUSDT_market_data.csv')

sentiment_data['timestamp'] = pd.to_datetime(sentiment_data['timestamp'], errors='coerce')
trading_data['date'] = pd.to_datetime(trading_data['Open Time'], errors='coerce')

sentiment_daily = sentiment_data.groupby(sentiment_data['timestamp'].dt.date).agg({
    'confidence': 'mean',
    'sentiment': lambda x: (x == 'POSITIVE').mean()
}).reset_index()


sentiment_daily['timestamp'] = pd.to_datetime(sentiment_daily['timestamp'])

merged_data = pd.merge(sentiment_daily, trading_data, left_on='timestamp', right_on='date', how='inner')

merged_data['sentiment'] = merged_data['sentiment'].map({'POSITIVE': 1, 'NEGATIVE': 0})

merged_data = merged_data.dropna(subset=['confidence', 'sentiment', '24hr Change'])

correlation = merged_data[['confidence', 'sentiment', '24hr Change']].corr(method='pearson')

print(correlation)

