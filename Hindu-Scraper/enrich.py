import nltk
import re
import csv
import heapq

def read_articles(filename):
	lines = []
	with open('newsT', 'r', newline='') as f:
		reader = csv.DictReader(f, fieldnames=['title','location','date','body'],delimiter='|')
		for line in reader:
			lines.append(line)
	return lines


def enrich(article):
	article_text = str(article['body'])
	article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
	article_text = re.sub(r'\s+', ' ', article_text)
	formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
	formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

	sentence_list = nltk.sent_tokenize(article_text)
	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}  
	for word in nltk.word_tokenize(formatted_article_text):  
		if word not in stopwords:
			if word not in word_frequencies.keys():
				word_frequencies[word] = 1
			else:
				word_frequencies[word] += 1
	if not word_frequencies:
		return {}
	article['keywords'] = word_frequencies.copy()
	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():  
		word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
	sentence_scores = {}  
	for sent in sentence_list:  
		for word in nltk.word_tokenize(sent.lower()):
			if word in word_frequencies.keys():
				if len(sent.split(' ')) < 30:
					if sent not in sentence_scores.keys():
						sentence_scores[sent] = word_frequencies[word]
					else:
						sentence_scores[sent] += word_frequencies[word]

	summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
	summary = ' '.join(summary_sentences)  
	article['summary'] = summary
	return article

articles = read_articles('newsT')
enriched_articles = [enrich(article) for article in articles]
with open('enriched_newsT','w',newline='') as f:
	writer = csv.DictWriter(f, fieldnames=enriched_articles[0].keys(),delimiter="|",extrasaction='ignore')
	writer.writeheader()
	for article in enriched_articles:
		writer.writerow(article)

