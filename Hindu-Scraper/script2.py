import requests
from bs4 import BeautifulSoup as bs
import lxml
from threading import Semaphore, Thread
from multiprocessing.dummy import Pool
import csv

screenlock = Semaphore(value=1)

with open('links.txt', 'r') as f:
	content = f.readlines()

def req_split(url):
	#requests.head is much faster than requests.get if your intention is only to get the status code
	html = requests.get(url) 
	return parseArticle(html)
	
def parseArticle(html):
	try:
		soup = bs(html.__dict__['_content'], "lxml")
		article = soup.select("[class~=article]")
		title = article[0].select("[class~=title]")
		title = title[0].get_text()
		body = article[0].select("[id*='content-body-']")
		time = soup.find("none").get_text()
		location = soup.find("span", class_="ksl-time-stamp").get_text().strip('\n').rstrip(',')
		item = {}
		item['time'] = time
		item['title'] = title
		item['location'] = location
		text = []
		for p in body[0].find_all("p"):
			text.append(p.get_text())
		item['body'] = " ".join(text).replace('\r', '').replace('\n', '')
		print(item['title'].rstrip() + '|' + item['location'] + '|' + item['time'].strip("\n")  + '|' + item['body'].rstrip())
	except:
		print("No article in ", str(html))

with Pool(150) as p:
	try:
		pm = p.imap_unordered(req_split,content)
		pm = [i for i in pm if i]
	except:
		print('error')

# with open('newsN2019.csv', 'w', newline='') as f:
# 	writer = csv.DictWriter(f, fieldnames=["title", "text"],delimiter="|")
# 	f.writeheader()
# 	for item in pm:
# 		f.writerow(item)

