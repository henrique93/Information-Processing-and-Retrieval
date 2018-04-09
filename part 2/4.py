import feedparser
from aux_func import *
from urllib.request import urlopen #import urllib2.urlopen
import xmltodict
resume =__import__('1')
from xml.etree import cElementTree as ET
import re

def exc4():
    nytRSS = "http://www.nytimes.com/services/xml/rss/nyt/World.xml" #"http://www.nytimes.com/services/xml/rss/index.html"
    cnnRSS = "http://rss.cnn.com/rss/edition_world.rss" #"http://edition.cnn.com/services/rss/"
    wpRSS = "http://feeds.washingtonpost.com/rss/world" #"https://www.washingtonpost.com/rss-feeds/2014/08/04/ab6f109a-1bf7-11e4-ae54-0cfe1f974f8a_story.html"
    laRSS = "http://www.latimes.com/world/rss2.0.xml" #"http://www.latimes.com/local/la-los-angeles-times-rss-feeds-20140507-htmlstory.html"

    rssPages = [nytRSS, cnnRSS, wpRSS, laRSS]
    rssFeed = []
    newsFeed = []

    for rss in rssPages:
        news = urlopen(rss)
        data = news.read()
        news.close()
        feed = feedparser.parse(data)
        rssFeed.append(feed)

        #print("NUMBER OF ENTRIES: " + str(len(feed['entries'])) + "\n")
        for post in feed.entries:
            sentence = ""
            hasTitle = False
            if hasattr(post, 'title') and (len(post.title) > 1):
                hasTitle = True
                title = post.title
                sentence = title
            if hasattr(post, 'description') and (len(post.description) > 1):
                description = post.description
                if hasTitle:
                    sentence += " "
                sentence += description
            if sentence != "":
                newsFeed.append(sentence)

    newsFeedFile = open("newsFeedFile.txt", "w")
    newsFeed = [text for text in newsFeed]
    for item in newsFeed:
        item = re.sub('<.*?>', '', item)
        newsFeedFile.write("%s\n" % item)
    newsFeedFile.close()
    blockPrint()
    top5 = resume.exc1("newsFeedFile.txt")
    enablePrint()
    for i in range(0, len(top5)):
        for feed in rssFeed:
            for post in feed.entries:
                news = ""
                hasTitle = False
                title = "Original article"
                if hasattr(post, 'title') and (len(post.title) > 1):
                    hasTitle = True
                    title = post.title
                    news = title
                if hasattr(post, 'description') and (len(post.description) > 1):
                    description = post.description
                    if hasTitle:
                        news += " "                    
                    news += description
                if news != "":
                    news = re.sub('<.*?>', '', news)
                    if top5[i] in news:
                        top5[i] += (' | From: ' + '<a href="' + post.link + '">' + title + '</a>')

    htmlFile = open("newsFeed.html", "w")
    htmlFile.write("<html>")
    htmlFile.write("<body><p>")
    htmlFile.write("The top five sentences are:\n")
    htmlFile.write("</br>")
    i = 0
    for sentence in top5:
        i += 1
        htmlFile.write(str(i) + " - " + sentence + "\n")
        htmlFile.write("</br>")

    htmlFile.write("</p></body>")
    htmlFile.write("<html>")
    htmlFile.close()