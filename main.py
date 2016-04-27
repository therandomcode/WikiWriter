
# ---------------------------------------------------------------- #
# WIKIWRITER
# Wikipedia Content Creation Assistant
# Created by Sharon Lin and Kristina Wagner
# Copyright April 2016
# ---------------------------------------------------------------- #

# Imports for Flask
import webapp2
import os
import jinja2
import json
import urllib2
import ssl
import requests
import httplib
from bs4 import BeautifulSoup

from google.appengine.ext.webapp.util import run_wsgi_app
#from app import app

# Import the Flask Framework
from flask import Flask, render_template_string, request, jsonify
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired 
app = Flask(__name__)
#app.secret_key = 'secret'

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])

index_html=''
with open("templates/index.html") as myfile:
    index_html = "".join(line.rstrip() for line in myfile)

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/topics')
def topics():
    key = str(request.args.get('key'))
    try: 
        anchors = []
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch="+key+"&srwhat=text&srprop=timestamp&continue"
        jsondata = urllib2.urlopen(url).read()
        print(jsondata)
        data = json.loads(jsondata)
        topics = [] 
        for item in data:
            val = data[item]
            if (item == "query"):
                for item2 in val:
                    val2 = val[item2]
                    if (item2 == "search"):
                        for item3 in val2:
                            p = (item3['title']).encode("utf-8")
                            topics.append(p)
    except:
        topics = ['Your topic sems to be unique! Congratulations!']
    return jsonify(topics=topics)

@app.route('/images')
def images():
    print "Starting images"
    key = str(request.args.get('key'))
    images = []
    
    print "trying this"
    key.replace (" ", "_")
    url = "http://www.bing.com/images/search?q="+key
    print(url)
    webpage = urllib2.urlopen(url)
    print("we just converted into htmldata")
    print webpage
    soup = BeautifulSoup(webpage, 'html.parser')
    #print(soup.prettify().encode('utf-8'))
    for tag in soup.find_all('img'):
        if "http" in tag["src"]:
            images.append(tag["src"])
    #images = ["We couldn't find any images. Try searching a different keyword!"]
    print images 
    return jsonify(images=images)



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
