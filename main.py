
# ---------------------------------------------------------------- #
# WIKIWRITER
# Wikipedia Content Creation Assistant
# Created by Sharon Lin and Kristina Wagner
# Copyright April 2016
# ---------------------------------------------------------------- #

# Imports for Flask
import webapp2
import cgi
#import MySQLdb
import os
import jinja2
import logging
import json
import urllib
import ssl
import requests
import socket
import httplib

from google.appengine.ext.webapp.util import run_wsgi_app
#from app import app

#Imports for Python -- these must be installed in the lib folder
import wikipedia

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
    print("look, we made it to here!")
    key = request.args.get('key')
    print(key)
    topics = wikipedia.search("bananas") or ['No topic found']
    #print(topics) 
    return jsonify(topics=topics)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
