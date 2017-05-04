#!/usr/bin/python

import urllib.request
import json
import argparse
import sys
from html.parser import HTMLParser

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class WikiItem:
    title = ""
    text = ""
    url = ""

class Http:
    def get(url, params):
        try:
            url_params = urllib.parse.urlencode(params)
            res = urllib.request.urlopen(url + url_params)
            return res.read()
        except:
            print("Http.get: Network is unreachable. ")
            return None

class Wikipedia:
    "Class for acess wikipedia API"
    lang = "en"
    format = "json"
    base_url = "https://en.wikipedia.org/wiki/"
    base_api_url = "https://en.wikipedia.org/w/api.php?"
    def __init__(self, lang = "en"):
        self.lang = lang
        self.base_url = "https://"+lang+".wikipedia.org/wiki/"
        self.base_api_url = "https://"+lang+".wikipedia.org/w/api.php?"
        return None
    def parseResponse_find(self, response):
        response = json.loads(response)
        resTitles = response[1]
        resDescr  = response[2]
        resUrl    = response[3]
        items = []
        for i in range( 0, len(resTitles) ):
            item = WikiItem()
            item.title = resTitles[i]
            item.text  = resDescr[i]
            item.url   = resUrl[i]
            items.append( item )
        return items
    def parseResponse_fullpage(self, title, response):
        response = json.loads(response)
        article = WikiItem()
        article.title = title
        article.text = strip_tags( response["mobileview"]["sections"][0]["text"] )
        article.url = self.base_url + article.title
        return [article]
    def find(self, query, count = 3):
        "Find term in wikipedia.org"
        res = Http.get(self.base_api_url, {
            'limit': count,
            'format': self.format,
            'action': 'opensearch',
            'search': query
        })
        if res == None:
            return []
        return self.parseResponse_find( res )
    def getFullpage(self, title):
        "Get full page content by title"
        res = Http.get(self.base_api_url, {
            'action': 'mobileview',
            'page': title,
            'sections': 0,
            'format': self.format
        })
        if res == None:
            return []
        return self.parseResponse_fullpage( title, res )

class Printer:
    def print(self, list):
        return None;
class CliPrinter(Printer):
    colorize = True
    def __init__(self, colorize):
        self.colorize = colorize
    def print(self, wikiItemsList):
        if wikiItemsList == None:
            return None
        for item in wikiItemsList:
            if self.colorize:
                print(colors.HEADER + item.title + colors.ENDC + " (" + colors.UNDERLINE + item.url + colors.ENDC + ")")
            else:
                print(item.title + " (" + item.url + ")")
            if( len(item.text) > 1 ):
                print(item.text)
            print("")

class Application:
    "The application class"
    wiki = None
    printer = Printer()
    args = None
    def __init__(self, argv):
        self.parseArgs(argv)
        self.wiki = Wikipedia(self.args.lang)
        self.printer = CliPrinter(self.args.color)
    def getParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('query')
        parser.add_argument("-l", "--lang", default="en", help="Set language for serach")
        parser.add_argument("-c", "--count", default=3, help="Limit search result")
        parser.add_argument("-e", "--extend", const=True, action="store_const", help="Get full article by title")
        parser.add_argument("--color", const=True, action="store_const", help="Colorize output")
        return parser
    def parseArgs(self, argv):
        parser = self.getParser()
        self.args = parser.parse_args(argv)
        return self.args
    def run(self):
        if not self.args.extend:
            items = self.wiki.find( self.args.query, self.args.count )
        else:
            items = self.wiki.getFullpage( self.args.query )
        self.printer.print(items)
        return 0

if __name__ == '__main__':
    Application(sys.argv[1:]).run()
