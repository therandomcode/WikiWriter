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

#check if in english
def is_ascii(s):
	return all(ord(c)<128 for c in s)

def getregarticles():
    #for finding regular articles:
    listB = []
    randomids = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=0&rnlimit=500").json()
    for i in range(500):
    	id = str(randomids['query']['random'][i]['id'])
    	url = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&pageids="+id+"&inprop=url").json()
    	pageurl = url['query']['pages'][id]['fullurl'].encode('utf-8')
    	print pageurl
    	page = urllib.urlopen(pageurl).read()
    	soup = BeautifulSoup(page)
    	goodindicator = (soup.find_all('div',{'id':'mw-indicator-good-star'})!=[])
    	featuredindicator = (soup.find_all('div',{'id':'mw-indicator-featured-star'})!=[])
    	if (goodindicator == True) or (featuredindicator==True):
    		print 'Article is Good or Featured' + id
    	elif (goodindicator == False) and (featuredindicator ==False):
    		print 'Article is Bad' + id
    		listB.append(pageurl[30:])
    		print listB
    return listB

#get list of articles from page
def getlinks(link):
	listA = []
	URL = urllib.urlopen(link).read()
	soup = BeautifulSoup(URL)
    #for finding good articles
	#data = soup.find_all('div',{'class': 'NavContent'})
    #for finding featured articles
	data = soup.find_all('td',style="padding:1em 1em 1em 1em; border:1px solid #A3BFB1; background-color:#F1F6FB")
	for div in data:
		links = div.find_all('a')
		for i in links:
			listA.append((i.get('href'))[6:])
	print listA
	return listA

#get 1000 random articles and save to file
def saveaslist(list):
	titlelist = []
	with open("listofarticles.txt", 'w') as f:
		for i in range(len(list)):
			index = random.randint(0,(len(list)-1))
			#index = i
			print list[index]
			if '/' in list[index]:
				article = urllib.quote(list[index],safe='')
				titlelist.append(article)
				f.write(article+",")
			elif is_ascii(list[index])==True:
				titlelist.append(list[index])
				f.write(list[index]+",")
			elif is_ascii(list[index])==False:
				print list[index] + "cannot be converted to utf-8"
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
	revisionsjson = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&list=&titles="+item+"&redirects=1&rvlimit=500&rvstart=2015-07-07T00%3A00%3A00.000Z&rvdir=newer").json()
	revisionsindex = '\n'.join(revisionsjson['query']['pages'].keys()).encode('utf-8')
	if 'revisions' in revisionsjson['query']['pages'][revisionsindex].keys():
		revisions = revisionsjson['query']['pages'][revisionsindex]['revisions']
		revisions_total = len(revisions)
	else:
		revisions_total = -1
	return revisions_total
#get all the pageviews for an article
def getpageviews(item):
	print item
	pageviews_total = 0
	pageviewsjson = requests.get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"+item+"/daily/20150701/20160410").json()
	print pageviewsjson.keys()
	try:
		pageviews = pageviewsjson['items']
	except KeyError:
		pageviews_total = "Not Available"
		return pageviews_total
	else:
		for j in range(len(pageviews)):
			pageviews_total = pageviews_total+pageviews[j]['views']
		return pageviews_total

#tabulate a bunch of data from the wikipedia page
def getwikidata(item):
	sec_total = 0
	ref_total = 0
	string = ''
	page = urllib.urlopen("https://en.wikipedia.org/wiki/"+item).read()
	soup = BeautifulSoup(page)
	dataimg = soup.find_all('a',{'class':'image'})
	img_total = len(dataimg)
	datacontents = soup.find_all('div', {'class':'toc'})
	datawords = soup.find_all('p')
	datarefs = soup.find_all('ol', {'class':'references'})
	text = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+item+"&redirects=1").json()
	textindex = '\n'.join(text['query']['pages'].keys()).encode('utf-8')
	paragraph = text['query']['pages'][textindex]['extract'].encode('utf-8')
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
	blob = TextBlob(string)
	numwords = len(blob.words)
	numsentences = len(blob.sentences)
	subjectivity = blob.sentiment.subjectivity
	polarity = blob.sentiment.polarity
	return(img_total,sec_total,ref_total,numwords,numsentences,subjectivity,polarity,paragraph)

#tabulate number of views for list of 500 random articles and put into csv
def dataforcsv(list):
	with open("PagesViews.csv", 'wb') as csvfile:
		fieldnames = ['Bin','Article Name','Number of Images', 'Number of Sections', 'Number of Sentences','Number of Words','Number of References','Subjectivity','Polarity','Paragraph','PagesViews','Revisions']
		writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
		writer.writeheader()
		for i in list:
			print i
			pv = getpageviews(i)
			#print pv
			rev = getrevisions(i)
			#print rev
			data = getwikidata(i)
			print data
			writer.writerow({'Bin': 'Regular', 'Article Name': i.encode('utf8'), 'Number of Images':data[0], 'Number of Sections': data[1], 'Number of Sentences': data[4],'Number of Words': data[3],'Number of References': data[2],'Subjectivity': data[5],'Polarity':data[6], 'Paragraph': data[7],'PagesViews':pv,'Revisions':rev})
		print "done"
				
linksC = getlinks("https://en.wikipedia.org/wiki/Wikipedia:Featured_articles")
#linksA = getlinks("https://en.wikipedia.org/wiki/Wikipedia:Good_articles/all")
#linksB1 = getregarticles()
#linksB2 = getregarticles()
#linksB3 = linksB1+linksB2
linkslist = saveaslist(linksC)
dataforcsv(linkslist)