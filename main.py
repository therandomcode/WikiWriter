import wikipedia
import categoryScraper

# ---------------------------------------------------------------- #
# WIKIWRITER
# Wikipedia Content Creation Assistant
# Created by Sharon Lin and Kristina Wagner
# Copyright April 2016
# ---------------------------------------------------------------- #

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
                        print (header)
                        headers.append(header)
        article = article[endIndex+2:]
    return headers


def getText():
    commonHeaders = [] 
    yourArticle = wikipedia.page("New York")
    articles = wikipedia.search("New York")
    for i in articles:
        article = wikipedia.page(i).content
        headers = getSectionHeaders(article)
        print headers
        for x in headers:
            if x not in commonHeaders:
                commonHeaders.append(x)
    for commonHeader in commonHeaders:
        print commonHeader
        
    # Figure out what kind of article this is
    # We can use the categories tag, if you've created it
    yourCategories = yourArticle.categories
    for category in yourCategories:
        #print category
        break

def main():
    print ("Hi and welcome to the command line interface!" )
    print ("I assume you'd like to write a Wikipedia Article.")
    topic = str(raw_input("What topic would you like to create an article about?"))
    print ("OK. Let me check and see if that exists already.")
    if (doesArticleExist(topic) != -1):
        if (int(raw_input("Is your article in the list? Please type 1 for yes and 0 for no")) == 1):
            if (int(raw_input("Do you want to search for another topic? Please type 1 for yes and 0 for no")) == 1):
                main()
            else:
                return
    print ("Great! Let's get started.")
    return 
