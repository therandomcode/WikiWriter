import json
import requests
import wikipedia
import os
import csv
import shutil
from bs4 import BeautifulSoup
import urllib
import random
from textblob import TextBlob

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


#turn articles to txt
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

#get all the revisions for an article
def getrevisions(item):
	revisionsjson = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&list=&titles="+item+"&rvlimit=500&rvstart=2015-07-07T00%3A00%3A00.000Z&rvdir=newer").json()
	revisionsindex = '\n'.join(revisionsjson['query']['pages'].keys()).encode('utf-8')
	revisions = revisionsjson['query']['pages'][revisionsindex]['revisions']
	revisions_total = len(revisions)
	return revisions_total
#get all the pageviews for an article
def getpageviews(item):
	pageviews_total = 0
	pageviews = requests.get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"+item+"/daily/20150701/20160410").json()
	pageviews = pageviews['items']
	for j in range(len(pageviews)):
		pageviews_total = pageviews_total+pageviews[j]['views']
	return pageviews_total

#tabulate a bunch of data from the wikipedia page
def getwikidata(item):
	img_total = 0
	sec_total = 0
	ref_total = 0
	string = ''
	page = urllib.urlopen("https://en.wikipedia.org/wiki/"+item).read()
	soup = BeautifulSoup(page)
	dataimg = soup.find_all('a',{'class':'image'})
	datacontents = soup.find_all('div', {'class':'toc'})
	datawords = soup.find_all('p')
	datarefs = soup.find_all('ol', {'class':'references'})
	for i in datarefs:
		li = i.find_all('li')
		for i in li:
			ref_total +=1
	for j in datawords:
		string += j.text
	for k in datacontents:
		li = k.find_all('li', {'class':'toclevel-1'})
		for l in li:
			sec_total+=1
	for m in dataimg:
		img = m.find_all('img')
		for n in img:
			img_total+=1
	blob = TextBlob(string)
	numwords = len(blob.words)
	numsentences = len(blob.sentences)
	return(img_total,sec_total,ref_total,numwords,numsentences)

#tabulate number of views for list of 500 random articles and put into csv
def dataforcsv(list):
	with open("PagesViews.csv", 'wb') as csvfile:
		fieldnames = ['Article Name', 'User Visits', 'Revisions', 'PPR','Number of Images', 'Number of Sections', 'Number of Sentences','Number of Words','Number of References']
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		writer.writeheader()
		for i in list:
			print i
			pv = getpageviews(i)
			print pv
			rev = getrevisions(i)
			print rev
			data = getwikidata(i)
			print data
			writer.writerow({'Article Name': i.encode('utf8'), 'User Visits': pv, 'Revisions': rev, 'PPR': pv/rev, 'Number of Images':data[0], 'Number of Sections': data[1], 'Number of Sentences': data[4],'Number of Words': data[3],'Number of References': data[2]})
		print "done"
				

dataforcsv(['Barack_Obama','Cell_theory'])