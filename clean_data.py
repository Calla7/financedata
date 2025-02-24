# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk



nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))



def clean_data(df):
    # 去重
    df = df.drop_duplicates()

    numeric_cols = df.select_dtypes(include=[np.number]).columns  # 数值型列
    non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns  # 非数值型列

    # 对数值型列使用均值填充
    imputer_numeric = SimpleImputer(strategy='mean')
    df[numeric_cols] = imputer_numeric.fit_transform(df[numeric_cols])

    # 对非数值型列使用最常见值填充
    imputer_non_numeric = SimpleImputer(strategy='most_frequent')
    df[non_numeric_cols] = imputer_non_numeric.fit_transform(df[non_numeric_cols])


    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    return df


stop_words = set(['the', 'is', 'in', 'and', 'to', 'of', 'a', 'on', 'at'])


def clean_text(text):

    text = text.lower()

    # 去除非字母数字字符
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # 去标点符号
    text = re.sub(r'[^\w\s]', '', text)

    # 去除停用词
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text


def clean_text_column(df, column_name):
    df[column_name] = df[column_name].apply(clean_text)
    return df


def scale_data(df, scaling_type='standardize'):
    if scaling_type == 'standardize':
        scaler = StandardScaler()  # 标准化
    elif scaling_type == 'normalize':
        scaler = MinMaxScaler()  # 使归一化

    numerical_columns = df.select_dtypes(include=[np.number]).columns
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    return df



def preprocess_files(file_paths, encoding='utf-8'):
    cleaned_dfs = []

    for file_path in file_paths:
        print(f"Processing {file_path}...")
        try:
            df = pd.read_csv(file_path, encoding=encoding, error_bad_lines=False)
        except UnicodeDecodeError:
            print(f"Error reading {file_path} with {encoding}. Trying 'ISO-8859-1'...")
            df = pd.read_csv(file_path, encoding='ISO-8859-1', error_bad_lines=False)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue


        df_cleaned = clean_data(df)

        if 'title' in df.columns:
            df_cleaned = clean_text_column(df_cleaned, 'title')

        # df_cleaned = scale_data(df_cleaned, scaling_type='standardize')

        cleaned_dfs.append(df_cleaned)

    return cleaned_dfs



file_paths = ['D:/pythonProject/financedata1/DataResource/market_sentiment_data.csv']


cleaned_data = preprocess_files(file_paths, encoding='utf-8')


for i, df in enumerate(cleaned_data):
    df.to_csv(f'cleaned_data_{i}.csv', index=False)
    print(f"Saved cleaned data to 'cleaned_data_{i}.csv'")