import json
import requests
import wikipedia
import os
import csv
import shutil
import BeautifulSoup
import urllib
import random

#get list of articles from page
def getlinks(url):
        listA = []
        URL = urllib.urlopen(url).read()
        soup = BeautifulSoup(URL)
        data = soup.find_all('div',{'class': 'NavFrame'})
        for div in data:
                links = div.find_all('a')
                for a in links:
                        listA.append(a.get('href'))[6:]
        return listA

#get 1000 random articles and save to file
def saveaslist(list):
        titlelist = []
        for i in range(1000):
                index = random.randint(0,(len(list)-1))
                titlelist.append(list[index])
        with open("listofarticles.txt", 'w') as f:
                f.write(titlelist)
        return titlelist


#get 1000 hundred random articles
def randomarticlestotxt(list):
	for i in list:
		try:
			f = open(i+".txt","w")
			f.write(wikipedia.page(title=i, auto_suggest=True).content.encode('utf8'))
		except wikipedia.exceptions.DisambiguationError:
			print "multiple articles for " + i
			os.remove(list[index]+".txt")
		except IOError:
			print "encoding error for " + i
		except wikipedia.exceptions.PageError:
			print "page not found for " + i
			os.remove(list[index]+".txt")
		else:
			f.close()


#tabulate number of views for list of 500 random articles and put into csv
def dataforcsv(list):
	with open("PagesViews.csv", 'wb') as csvfile:
		fieldnames = ['Article Name', 'User Visits', 'Revisions', 'PPR','Number of Images','Number of Words']
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
				revisions_total = len(revisions)
			except KeyError:
				#pageviews = pageviews['items']
				pageviews_total = 'None'
				revisions_total = 'None'
				#revisions_total = 1
			'''else:
				for j in range(len(pageviews)):
					pageviews_total = pageviews_total+pageviews[j]['views']
				PPR = pageviews_total/revisions_total
				writer.writerow({'Article Name': i.encode('utf8'), 'User Visits': pageviews_total, 'Revisions': revisions_total, 'PPR': PPR})
				if PPR >= 7000:
					bin = '7000+'
				elif 2500<=PPR < 7000:
					bin = '2500-7000'
				elif 1000<=PPR < 2500:
					bin = '1000-2500'
				elif 500<=PPR < 1000:
					bin = '500-1000'
				elif PPR<500:
					bin = '0-500'
				else:
					print "error PPR not a number"
				try:
					shutil.move("/Users/superstah/documents/05-839/WikiWriter/"+i+".txt","/Users/superstah/documents/05-839/WikiWriter/"+bin+"/"+i+".txt")
				except SyntaxError:
					print "non ascii character"
				except IOError:
					print j, "weird utf-8 problem"'''
rand = wikipedia.random(pages=60)
randomarticlestotxt(rand)
getpageviewstocsv(rand)
