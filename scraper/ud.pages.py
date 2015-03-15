#!/usr/bin/env python
import xml.dom.minidom as domParser
import urllib2, gzip, zlib, os, urllib
from StringIO import StringIO
from bs4 import BeautifulSoup
import time
import sys

def fetch_ud_page(term, cache = True):
    request = urllib2.Request('http://www.urbandictionary.com/define.php?term=' + urllib.quote_plus(term.encode('utf-8')))
    request.add_header('Accept-encoding', 'gzip')
    try:
        response = urllib2.urlopen(request)
    except Exception:
        return None
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
    if cache:
        with open("data/" + term.encode("utf-8").replace("/","_B_").replace("\\","_F_") + ".crawl", "w") as f:
            f.write(data)
    # Decide if this is a valid page or not
    soup = BeautifulSoup(data.decode('utf-8'))
    collection = soup.find_all("div", class_="def-panel")
    if len(collection) == 0:
        return None
    else:
        definitions = []
        for panel in collection:
            l = panel.find_all("div", class_="meaning")
            r = panel.find_all("div", class_="example")
            u = panel.find_all("a", class_="thumb up")
            d = panel.find_all("a", class_="thumb down")
            uv, dv = None, None
            if len(u) > 0 and len(d) > 0:
                try:
                    uv = int(u[0].text.strip())
                    dv = int(d[0].text.strip())
                except Exception:
                    # Do nothing
                    sys.stderr.write("! Could not read ranking for word\n")
            if len(l) > 0 and len(r) > 0:
              definitions.append({
                "meaning": l[0].text.strip().replace("\n"," ").replace("\r",""),
                "example": r[0].text.strip().replace("\n"," ").replace("\r",""),
                "votes": (uv, dv)
              })
        return definitions

def fetch_all_pages(wordsfile, filename = "default", skip = 0, logfile=None):
    words = []
    with open(wordsfile, "r") as g:
        for line in g:
            if skip > 0:
                skip -= 1
                continue;
            words.append(line.decode("utf-8").strip())
    
    with open(filename, 'w') as f:
        gotwords = 0
        for word in words:
            sys.stderr.write("+ Writing page %s\n" % word)
            defs = fetch_ud_page(word)
            if defs == None:
                if logfile != None:
                    logfile.write(word.encode("utf-8") + "\n");
                continue
            for defn in defs:
                f.write("|||".join([word,defn["meaning"],defn["example"],",".join(str(i) for i in defn["votes"])]).encode("utf-8") + "\n")
            gotwords += 1
            if gotwords % 10 == 0:
                sys.stderr.write("+ Sleeping ...\n")
                time.sleep(2)
            if gotwords % 100 == 0:
                sys.stderr.write("+ Long Wait ... \n")
                time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "pages [words-file] [output-filename] [skip]"
    else:
        with open(sys.argv[2] + '.err.log', 'w') as l:
            fetch_all_pages(sys.argv[1], sys.argv[2], 0 if len(sys.argv) == 3 else sys.argv[1], l)
