import xml.dom.minidom as domParser
import urllib2, gzip, zlib, os
from StringIO import StringIO
from bs4 import BeautifulSoup
import time
import sys

def fetch_ud_page(char =  'A', page = 1):
    request = urllib2.Request('http://www.urbandictionary.com/browse.php?character=' + char + '&page=' + str(page))
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
    collection = soup.find_all("div", class_="collection-panel")
    if len(collection) == 0:
        return None
    else:
        words = []
        for panel in collection:
            l = panel.find_all("a")
            for possibleword in l:
                if possibleword.has_attr("href") and "/define" in possibleword['href']:
                    words.append(possibleword.text)
        return words

def fetch_all_pages(char = 'A'):
    with open(char + ".tsv", 'w') as f:
        page = fetch_ud_page(char, 1)
        cur = 1
        while page != None:
            sys.stderr.write("+ Writing page %i\n" % cur)
            for pdata in page:
                f.write(pdata.strip().encode("utf-8").strip())
                f.write("\n")
            cur += 1
            if cur % 10 == 0:
                sys.stderr.write("* Sleeping...\n")
                time.sleep(5)
            page = fetch_ud_page(char, cur)

if __name__ == "__main__":
   fetch_all_pages(sys.argv[1])
