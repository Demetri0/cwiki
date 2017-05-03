#!/usr/bin/python

import urllib.request
import json
import argparse
import sys

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WikiItem:
    title = ""
    text = ""
    url = ""

class Wikipedia:
    "Class for acess wikipedia API"
    lang = "en"
    def __init__(self, lang = "en"):
        self.lang = lang
        return None
    def parseResponse(self, response):
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
    def find(self, query, count = 3):
        "Find term in wikipedia.org"
        params = {
            'limit': count,
            'format': 'json',
            'action': 'opensearch',
            'search': query
        }
        url_params = urllib.parse.urlencode(params)
        res = urllib.request.urlopen("http://"+self.lang+".wikipedia.org/w/api.php?" + url_params)
        #res = urllib.request.urlopen("http://"+self.lang+".wikipedia.org/w/api.php?action=opensearch&format=json&search="+query)
        return self.parseResponse( res.read() )

class CliPrinter:
    def print(self, wikiItemsList):
        for item in wikiItemsList:
            print(colors.HEADER + item.title + colors.ENDC + " (" + colors.UNDERLINE + item.url + colors.ENDC + ")")
            if( len(item.text) > 1 ):
                print(item.text)
            print("")

class Application:
    "The application class"
    wiki = None
    printer = None
    args = None
    def getParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('query')
        parser.add_argument("-l", "--lang", default="en",
                help="Set language for serach")
        parser.add_argument("-c", "--count", default=3,
                help="Limit search result")
        return parser
    def parseArgs(self, argv):
        parser = self.getParser()
        self.args = parser.parse_args(argv)
        return self.args
    def __init__(self, argv):
        self.parseArgs(argv)
        self.wiki = Wikipedia(self.args.lang)
        self.printer = CliPrinter()
    def run(self):
        items = self.wiki.find( self.args.query, self.args.count )
        self.printer.print(items)
        return 0

if __name__ == '__main__':
    Application(sys.argv[1:]).run()
