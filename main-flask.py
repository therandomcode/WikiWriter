
# ---------------------------------------------------------------- #
# WIKIWRITER
# Wikipedia Content Creation Assistant
# Created by Sharon Lin and Kristina Wagner
# Copyright April 2016
# ---------------------------------------------------------------- #

# Imports for Flask
import webapp2
import cgi
import MySQLdb
import os
import jinja2
import logging
import json
import urllib
from google.appengine.ext.webapp.util import run_wsgi_app

#Imports for Python
import wikipedia

# Import the Flask Framework
from flask import Flask
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

def searchPressed(topic):
	if doesArticleExist(topic) == -1:
		#The article didn't exist. Do something
	else:
		sim_articles = foundTopics
		return render_template("index.html")

# First you want to find out if the article has been created
def doesArticleExist(topic):
    foundTopics = wikipedia.search(topic)
    print("We found the following articles for " + topic)
    if (len(foundTopics) > 10):
        maxcounter = 10;
    elif (len(foundTopics) != 0):
        maxcounter = len(foundTopics)
    else:
        print ("No topics were found! Your topic is new!") 
        return -1 
    for counter in range(maxcounter):
        print(foundTopics[counter])
    return foundTopics

#Note that subheaders always begin with "="
def getSectionHeaders(article):
    headers = []
    startIndex = 0
    while startIndex != -1:
        #Find Start
        startIndex = article.find("==")
        #Find end
        subarticle = article[startIndex+2:]
        endIndex = subarticle.find("==")
        if ((startIndex > -1) and (endIndex > -1)):
            if (startIndex != endIndex):
                if (endIndex - startIndex < 100 and endIndex > startIndex):
                    header = article[startIndex+2:startIndex+2+endIndex]
                    header = header.strip(' \t\n\r')
                    if header != "" and header != "\n" and header != "=":
                        headers.append(header)
        article = article[endIndex+2:]
    return headers

def getText():
    commonHeaders = []
    popularity = []
    yourArticle = wikipedia.page("Obama")
    articles = []
    articles.append(wikipedia.search("American politicans"))
    articles.append(wikipedia.search("American presidents"))
    articles.append(wikipedia.search("Hillary Clinton"))
    articles.append(wikipedia.search("Bill Clinton"))
    articles.append(wikipedia.search("George Washington"))
    articles.append(wikipedia.search("John Kerry"))
    #articles.append(wikipedia.search("John F. Kennedy"))
##    yourArticle = wikipedia.page("New York")
##    articles = wikipedia.search("New York")
##    articles.append(wikipedia.search("American cities"))
##    articles.append(wikipedia.search("Boston"))
##    articles.append(wikipedia.search("Paris"))
##    articles.append(wikipedia.search("San Francisco"))
##    articles.append(wikipedia.search("Sacramento"))
##    articles.append(wikipedia.search("Seattle"))
##    articles.append(wikipedia.search("Chicago"))
##    articles.append(wikipedia.search("St. Louis"))
##    articles.append(wikipedia.search("Las Vegas"))
##    articles.append(wikipedia.search("Hartford"))
##    articles.append(wikipedia.search("Trenton, NJ"))
##    articles.append(wikipedia.search("Washington D.C."))
##    articles.append(wikipedia.search("Boise"))
##    articles.append(wikipedia.search("Detroit"))
##    articles.append(wikipedia.search("Now Orleans"))
##    articles.append(wikipedia.search("Salt Lake City"))
    for i in articles:
        article = wikipedia.page(i).content
        headers = getSectionHeaders(article)
        for x in headers:
            if x not in commonHeaders:
                commonHeaders.append(x)
                popularity.append(1)
            else:
                assert(len(popularity) > 1) 
                popularity[commonHeaders.index(x)] += 1
                print x
    print commonHeaders
    x = 0
    while (x < len(commonHeaders)):
        if (popularity[x]>1):
            print commonHeaders[x]
            print popularity[x]
        x = x + 1
        
    # Figure out what kind of article this is
    # We can use the categories tag, if you've created it
    yourCategories = yourArticle.categories
    for category in yourCategories:
        #print category
        break
    return 

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
