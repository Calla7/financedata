import csv
import gensim
from gensim import corpora
import nltk
import string
import csv



# 话题建模
def topic_modeling(texts, num_topics=3):
    texts_cleaned = []
    for text in texts:
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = nltk.word_tokenize(text.lower())
        texts_cleaned.append(words)

    dictionary = corpora.Dictionary(texts_cleaned)
    corpus = [dictionary.doc2bow(text) for text in texts_cleaned]

    lda_model = gensim.models.LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    topics = []
    for idx, topic in lda_model.print_topics(-1):
        topics.append(topic)

    return topics


def process_data(file_path, output_path=None):
    try:
        sentiment_results = []
        topics = []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                text = row.get('title')
                if text:
                    topics_for_text = topic_modeling([text], num_topics=3)
                    topics.append({'text': text, 'topics': topics_for_text})

        print("\nTopic Modeling (LDA):")
        for idx, result in enumerate(topics):
            print(f"Text: {result['text']}")
            print(f"Topics: {result['topics']}")
            print("-" * 40)

        if output_path:
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['text', 'topics'])
                writer.writeheader()
                for result in topics:
                    writer.writerow(result)

    except Exception as e:
        print(f"An error occurred: {e}")

file_path = 'D:/pythonProject/financedata1/DataClean/cleaned_market_sentiment_data.csv'
output_path = 'D:/pythonProject/financedata1/DataClean/topic_modeling_results.csv'  # 输出结果保存的CSV文件路径
process_data(file_path, output_path)