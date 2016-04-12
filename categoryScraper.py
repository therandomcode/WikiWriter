import wikipedia

# ---------------------------------------------------- #
# WikiWriter
# Section Scrapers
# By Kristina Wagner and Sharon Lin
# Copyright April 2016
# -----------------------------------------------------#

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

article = wikipedia.page("Obama").content
getSectionHeaders(article)
