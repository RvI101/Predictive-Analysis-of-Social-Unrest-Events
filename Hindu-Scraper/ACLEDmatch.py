import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

newsdata = pandas.read_csv('enriched_newsT')
acldata = pandas.read_csv('2019-01-01-2019-01-30-India.csv')

def cosine_Similarity(data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    cosine_mat = (X * X.T).A
    return cosine_mat