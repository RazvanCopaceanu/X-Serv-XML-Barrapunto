#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.file = open("contenidos.html", "w")
        self.line = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = "Titulo de la noticia: " + self.theContent + "."
                # To avoid Unicode trouble
                print (self.line)
                self.file.write(self.line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = self.theContent
                links = "<p>Enlace noticia: <a href='" + self.link + "'>" + self.link + "</a></p>\n"
                print (links)
                self.file.write(links)
                self.inContent = False
                self.theContent = ""
                self.link = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

            
# --- Main prog

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

url = "http://barrapunto.com/index.rss"
xmlStream = urllib.request.urlopen(url)
theParser.parse(xmlStream)

print ("Parse complete")