import json
import requests
import wikipedia
import os
import csv


#get five hundred random articles
def randomarticlestotxt(list):
	for i in list:
		try:
			f = open(i+".txt","w")
			f.write(wikipedia.page(title=i, auto_suggest=True).content.encode('utf8'))
		except wikipedia.exceptions.DisambiguationError:
			print "multiple articles for " + i
			os.remove(i+".txt")
		except IOError:
			print "encoding error for " + i
		except wikipedia.exceptions.PageError:
			print "page not found for " + i
			os.remove(i+".txt")
		else:
			f.close()

#tabulate number of views for list of 500 random articles and put into csv
def getpageviewstocsv(list):
	with open("PagesViews.csv", 'wb') as csvfile:
		fieldnames = ['Article Name', 'User Visits', 'Revisions']
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		writer.writeheader()
		for i in list:
			print i
			pageviews_total = 0
			revisions_total = 0
			pageviews = requests.get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"+i+"/daily/20150701/20160410").json()
			revisions = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&list=&titles="+i+"&rvlimit=500&rvstart=2015-07-07T00%3A00%3A00.000Z&rvdir=newer").json()
			revisionsindex = '\n'.join(revisions['query']['pages'].keys()).encode('utf-8')
			try:
				revisions = revisions['query']['pages'][revisionsindex]['revisions']
				pageviews = pageviews['items']
			except KeyError:
				print "No revisions found for " + i
				revisions_total = 'None'
				pageviews_total = 'None'
			else:
				revisions_total = len(revisions)
				for j in range(len(pageviews)):
					pageviews_total = pageviews_total+pageviews[j]['views']
				writer.writerow({'Article Name': i.encode('utf8'), 'User Visits': pageviews_total, 'Revisions': revisions_total})

rand = wikipedia.random(pages=500)
#randomarticlestotxt(rand)
getpageviewstocsv(rand)
