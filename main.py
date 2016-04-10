import wikipedia

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

def getText():
    # So ideally here we would have an online text editor that allows you to write the article in the cloud as well
    # But for the sake of the argument we're going to assume you can copy and paste text into this

    # Let's take some example text
    yourArticle = wikipedia.page("New York")

    # Figure out what kind of article this is
    # We can use the categories tag, if you've created it
    yourCategories = yourArticle.categories
    for category in yourCategories:
        print category

    # Starting with some sub categories
    people = ["Authors", "Leaders", "Legends"]
    places = ["Fantasy", "Continent", "Country", "City", "Monument"]
    events = ["Battle", "Political", "Historical"]
    animals = ["Mammal", "Bird", "Fish", "Insect"]
    
    # Now making a category for categories #MetaLife
    categories = [people, places, events, animals]

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
