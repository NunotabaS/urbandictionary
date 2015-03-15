import xml.dom.minidom as domParser
import urllib2, gzip, zlib, os
from StringIO import StringIO
from bs4 import BeautifulSoup
import time
import sys

def fetch_osd_page(listname = '0-a'):
    request = urllib2.Request('http://onlineslangdictionary.com/word-list/' + listname + '/')
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    data = None
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    elif response.info().get('Content-Encoding') == 'deflate':
        data = zlib.decompressobj(-zlib.MAX_WBITS).decompress(response.read())
    else:
        data = response.read()
    if data == None:
        raise Exception("Could not read page");
    # Decide if this is a valid page or not
    soup = BeautifulSoup(data.decode('utf-8'))
    collection = soup.find_all("table", class_="wordlist")
    if len(collection) == 0:
        return None
    else:
        words = []
        for panel in collection:
            l = panel.find_all("a")
            for possibleword in l:
                if possibleword.has_attr("href") and "/meaning-definition-of" in possibleword['href']:
                    words.append(possibleword.text)
        return words

def fetch_all_pages(filename):
    PAGES = ['0-a', 'b-b', 'c-d', 'e-f', 'g-g', 'h-k', 'l-o', 'p-r', 's-s', 't-t', 'u-w', 'x-z']
    with open(filename + ".tsv", 'w') as f:
        for pageRange in PAGES:
            page = fetch_osd_page(pageRange)
            sys.stderr.write("+ Writing page %s\n" % pageRange)
            if page != None:
                for word in page:
                    f.write(word.strip().encode('utf-8') + "\n")

if __name__ == "__main__":
   fetch_all_pages(sys.argv[1])



