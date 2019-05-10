import csv
import json
from tweet_search import TwitterContextSearch
import sentiment
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import time
from datetime import datetime, timedelta
import ast
from threading import Semaphore, Thread
from multiprocessing.dummy import Pool
import en_core_web_lg
from spacy.matcher import Matcher
nlp = en_core_web_lg.load()


newsdf = pd.read_csv('Predictive-Analysis-for-protests-riots/Hindu-Scraper/filteredDataset.csv')
newsdf.loc[:,'Pos'] = None
newsdf.loc[:,'Neu'] = None
newsdf.loc[:,'Neg'] = None

numbers = [n for n in range(newsdf.shape[0])]

search = TwitterContextSearch()

def tweetsForRow(index):
	row = newsdf.iloc[[index]]
	article_date = datetime.fromisoformat(row.get('date'))
	since = (article_date - timedelta(days=50)).strftime("%Y-%m-%d")
	until = (article_date + timedelta(days=50)).strftime("%Y-%m-%d")
	body = row.get('body')
	print(index)
	doc = nlp(body)
	print(doc)
	entities = [e.text for e in doc.ents if e[0].ent_type_ in ['ORG', 'GPE', 'PERSON']]
	print(entities)
	query_string = " OR ".join(entities)
	print(query_string)
	tweets = search.searchTweets(query_string, since, until, 50)
	if len(tweets) == 0:
		return
	print(len(tweets))
	p,n,ne = sentiment.getSentimentFeature(tweets)
	print(p,n,ne)
	newsdf.at[index,'Pos'],newsdf.at[index, 'Neg'],newsdf.at[index, 'Neu'] = p,n,ne

with Pool(150) as p:
	try:
		p.imap_unordered(tweetsForRow,numbers)
		newsdf.to_csv('hindusents.csv', header=True)
	except:
		print('error')