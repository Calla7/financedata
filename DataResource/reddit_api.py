# -*- coding: utf-8 -*-
import praw
import time
import pandas as pd
from datetime import datetime
import os
import sys
import codecs


sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

client_id = 'FlMyqOMWWMeRjhwMGqxqWg'
client_secret = 'Ad8Pc9R-oEkuGEC19C_ROIBVIKzOEA'
user_agent = 'financedata by /u/Old_Obligation_7578'

# Reddit认证
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

keywords = ['stock', 'cryptocurrency', 'bitcoin', 'Tencent', 'Apple', 'Google']

columns = ['keyword', 'title', 'author', 'score', 'created_utc']

csv_file = 'market_sentiment_data.csv'

def save_to_csv(data):
    df = pd.DataFrame(data, columns=columns)

    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False, encoding='utf-8')  # 文件存在时，不写入表头
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False, encoding='utf-8')  # 文件不存在时，写入表头

subreddit = reddit.subreddit('all')

all_post_data = []
for keyword in keywords:
    print(f"搜索关键词：{keyword}")

    for submission in subreddit.search(keyword, limit=10):

        post_data = {
            'keyword': keyword,
            'title': submission.title,
            'author': str(submission.author),
            'score': submission.score,
            'created_utc': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        }

        print(f"标题: {submission.title}")
        print(f"链接: {submission.url}")
        print(f"作者: {submission.author}")
        print(f"赞同数: {submission.score}")
        print(f"创建时间: {datetime.utcfromtimestamp(submission.created_utc)}")
        print("-" * 50)

        all_post_data.append(post_data)

        time.sleep(1)

save_to_csv(all_post_data)
print("数据已成功存储到 CSV 文件。")

