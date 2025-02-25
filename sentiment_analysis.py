import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline

local_model_path = r'D:/huggingface/models/distilbert-base-uncased-finetuned-sst-2-english'

model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
tokenizer = AutoTokenizer.from_pretrained(local_model_path)

emotion_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# 情绪分析
def sentiment_analysis(texts, timestamps):
    sentiment_results = []
    for text, timestamp in zip(texts, timestamps):
        sentiment = emotion_analyzer(text)
        label = sentiment[0]['label']
        score = sentiment[0]['score']
        sentiment_results.append({
            'text': text,
            'sentiment': label,
            'confidence': score,
            'timestamp': timestamp
        })
    return sentiment_results

def process_data(file_path, output_path):
    try:
        sentiment_results = []
        # 使用 chunksize 分批读取数据
        chunksize = 1000
        for chunk in pd.read_csv(file_path, usecols=['title', 'created_utc'], chunksize=chunksize):

            texts = chunk['title'].dropna().tolist()
            timestamps = chunk['created_utc'].dropna().tolist()

            sentiment_results.extend(sentiment_analysis(texts, timestamps))

        print("Sentiment Analysis Results:")
        for result in sentiment_results:
            print(f"Text: {result['text']}\nSentiment: {result['sentiment']}, Confidence: {result['confidence']:.4f}, Timestamp: {result['timestamp']}\n")

        result_df = pd.DataFrame(sentiment_results)
        result_df.to_csv(output_path, index=False)

        print(f"Sentiment analysis results have been saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

input_file_path = 'D:/pythonProject/financedata1/DataClean/cleaned_market_sentiment_data.csv'
output_file_path = 'D:/pythonProject/financedata1/SentimentAnalyse/sentiment_analysis_results.csv'

process_data(input_file_path, output_file_path)