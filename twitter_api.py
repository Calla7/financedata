import requests
import time
import json
import pandas as pd
from datetime import datetime

bearer_token = "AAAAAAAAAAAAAAAAAAAAABeTzgEAAAAA926xncdnzWHzWBAK5pbS4hNnYcE%3D5RdqvOpFkzApYhnZ1R4MgWvFOTEjiejX02pLbbuHEiqEptzfyG"
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}
url = 'https://api.twitter.com/2/tweets/search/recent'


def fetch_tweets_past_week(query, max_results=100):
    all_tweets = []
    next_token = None

    for _ in range(7):
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,text'
        }
        if next_token:
            params['next_token'] = next_token

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            tweets = data.get("data", [])
            all_tweets.extend(tweets)
            next_token = data.get("meta", {}).get("next_token")
            if not next_token:
                break
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 15 minutes...")
            time.sleep(900)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    return all_tweets


tickers = ["TSLA", "NVDA", "GOOGL", "BABA", "AAPL", "MSFT"]


def fetch_tweets_for_all_tickers():
    print("Fetching tweets for all stocks...")
    all_tweets = []

    for ticker in tickers:
        tweets = fetch_tweets_past_week(f"{ticker} stock")
        tweet_data = [(tweet['created_at'], ticker, tweet['text']) for tweet in tweets]
        df_tweets = pd.DataFrame(tweet_data, columns=["timestamp", "ticker", "text"])
        df_tweets["timestamp"] = pd.to_datetime(df_tweets["timestamp"]).dt.date  # 转换为日期格式
        all_tweets.append(df_tweets)

    if all_tweets:
        tweets_df_final = pd.concat(all_tweets, ignore_index=True)
        tweets_df_final.to_csv("twitter_sentiment_data.csv", index=False)
        print("Data saved to twitter_sentiment_data.csv")
        return tweets_df_final
    return None


tweets_data = fetch_tweets_for_all_tickers()
