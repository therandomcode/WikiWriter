index_html = ""
with open("templates/index.html") as myfile:
    index_html = "".join(line.rstrip() for line in myfile)
    print(index_html)

    
@app.route('/')
#This is for the version that uses Ajax
def index():
    return render_template_string(index_html, topics = None, form = WikiForm())

#This is for the pure HTML version of this app 
def index5():
    form = WikiForm() 
    print(form)
    if form.validate_on_submit():
        topics = wikipedia.search(form.key.data) or ['No topics found']
        return render_template_string(index_html, topics = topics, form = form)
    return render_template_string(index_html, topics = None, form = form)

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    key = request.args.get('key')
    topics = wikipedia.search(key) or ['No topics found']
    #return render_template_string(index_html, topics = topics, form = form)
    return jsonify(topics = topics)

@app.route('/index')
# First you want to find out if the article has been created
def index2():
    topic = "cats"
    foundTopics = wikipedia.search(topic)
    if (len(foundTopics) > 0):
        print("This is being called")
        return render_template('index.html', foundTopics = foundTopics)
        #return foundTopics
    return ["No topics were found! Your topic is new!"]

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
