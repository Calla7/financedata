import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 关键词提取
def extract_keywords_tfidf(texts, top_n=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    feature_names = np.array(vectorizer.get_feature_names_out())
    keywords = []
    for i in range(X.shape[0]):
        sorted_indices = np.argsort(X[i].toarray()).flatten()[::-1]
        top_keywords = feature_names[sorted_indices[:top_n]]
        keywords.append(top_keywords)
    return keywords

# 词云
def generate_wordcloud(keywords):

    all_keywords = ' '.join([', '.join(keyword) for keyword in keywords])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_keywords)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    wordcloud_image_path = 'D:/pythonProject/financedata1/SentimentAnalyse/wordcloud.png'
    wordcloud.to_file(wordcloud_image_path)
    print(f"\nWord cloud image saved to {wordcloud_image_path}")

def process_data(file_path, output_path):
    sentiment_results = []
    keywords = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                text = row.get('title')
                if text:
                    keyword = extract_keywords_tfidf([text], top_n=5)
                    keywords.append(keyword[0])
                    sentiment_results.append(text)

        print("\nKeyword Extraction (TF-IDF):")
        for i, text in enumerate(sentiment_results):
            print(f"Text: {text}\nTop Keywords: {', '.join(keywords[i])}\n")

        if output_path:
            output_data = []
            for i, text in enumerate(sentiment_results):
                output_data.append({
                    'Text': text,
                    'Top Keywords': ', '.join(keywords[i])
                })
            df = pd.DataFrame(output_data)
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"\nResults saved to {output_path}")

        generate_wordcloud(keywords)

    except Exception as e:
        print(f"An error occurred: {e}")

file_path = 'D:/pythonProject/financedata1/DataClean/cleaned_market_sentiment_data.csv'
output_path = 'D:/pythonProject/financedata1/SentimentAnalyse/TFIDF_results.csv'
process_data(file_path, output_path)