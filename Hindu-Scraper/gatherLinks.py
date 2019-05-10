# Author: Ranjodh Singh

import requests
from bs4 import BeautifulSoup as bs
import os
import csv

def is_a_href_2019(tag):
	return tag.name == 'a' and '2019' in tag['href']

def is_Apr_2019(tag):
	return tag.name == 'a' and '2019/04/' in tag['href']

def is_a_no_class(tag):
	return tag.name == 'a' and not tag.has_attr('class')

def parse_articles(links):
	items = []
	for c in range(len(links)):
		try:
			html = requests.get(links[c][:-1])
			soup = bs(html.__dict__['_content'], "html5lib")
			article = soup.select("[class~=article]")
			title = article[0].select("[class~=title]")
			title = title[0].get_text()
			body = article[0].select("[id*='content-body-']")
			item = {}
			item['title'] = title
			text = []
			for p in body[0].find_all("p"):
					text.append(p.get_text())
			item['body'] = " ".join(text)
			items.append(item)
		except:
			print("No article in ", str(links[c][:-1]))
	return items

url = "http://www.thehindu.com/archive/"
html = requests.get(url)
soup = bs(html.__dict__['_content'], "html5lib")
container = soup.select("#archiveTodayContainer")
links = []
for link in container[0].find_all(is_Apr_2019):
	resp = requests.get(link['href'])
	soup = bs(resp.__dict__['_content'], "html5lib")
	daily_links = soup.select("[class~=ui-state-default]")
	for l in daily_links:
		web_link = l['href']
		s = bs(requests.get(web_link).__dict__['_content'], "html5lib")
		paper_container = s.find("div", class_="tpaper-container")

		news_links = paper_container.find_all(is_a_no_class)
		news_links = [i['href'] for i in news_links]
		try:
			print(news_links[-2], news_links[-1])
		except IndexError:
			print('no articles, skipping')
			continue
		links.extend(news_links)
		# for n in range(len(news_links)):
		#     news = bs(requests.get(web_link + news_links[n]['href']).__dict__['_content'], "html5lib")
		#     try:
		#         headline = news.find("h3").get_text()
		#     except:
		#         headline = ""
		#     with open(new_dir + "/" + str(n) + ".txt", "w") as f:
		#         f.write(headline)
		#         for x in news.find_all('p')[:-4]:
		#             f.write(x.get_text())

with open('links.txt', 'w') as f:
	for link in links:
		f.write(str(link) + "\n")


# items = parse_articles(links)
# with open('news2019.csv', 'w', newline='') as f:
# 	writer = csv.DictWriter(f, fieldnames=["title", "text"],delimiter="|")
# 	f.writeheader()
# 	for item in items:
# 		f.writerow(item)