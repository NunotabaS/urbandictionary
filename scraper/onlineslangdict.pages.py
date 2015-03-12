import xml.dom.minidom as domParser
import urllib2, gzip, zlib, os, urllib, re
from StringIO import StringIO
from bs4 import BeautifulSoup
import time
import sys

def fetch_osd_page(listname):
    modname = re.sub(r"%", "%25", re.sub(r"\s", '-',listname.encode('utf-8')))
    modname = re.sub(r"/", "%2f", modname)
    request = urllib2.Request('http://onlineslangdictionary.com/meaning-definition-of/' + urllib.quote_plus(modname) + '')
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
    collection_nf = soup.find_all("div", class_="term-non-featured")
    collection_f = soup.find_all("div", class_="term-featured")
    if len(collection_nf) == 0:
        collection = collection_f
    else:
        collection = collection_nf
    if len(collection) == 0:
        return None
    else:
        words = []
        for panel in collection:
            l = panel.find_all("h2")
            bin = None
            if len(l) > 0:
                bin = l[0].text
            else:
                bin = listname
            defs = panel.find_all("div", class_="definitions")
            if len(defs) == 0:
                return None
            pos, defn = None, None
            for elem in defs[0].contents:
                if elem.name == None:
                    continue
                if elem.name.lower() == "h3":
                    pos = re.sub(r"[\r\n]", "", elem.text.strip())
                elif elem.name.lower() == "ul":
                    for definition in elem.contents:
                        if definition.name == "li":
                            defn = "".join([d for d in definition.contents if d.name == None])
                            defn = re.sub(r"[\r\n]"," ", defn).strip()
                            words.append((listname, bin, pos if pos != None else "", defn))
                    pos, defn = None, None
                else:
                    print elem.name
        return words

def fetch_all_pages(filename, outfile, errfile):
    with open(filename, 'r') as f:
        with open(outfile, 'w') as g:
            count = 0
            for line in f:
                count+= 1
                word = line.strip().lower()
                sys.stderr.write(" + Getting word %d, %s...\n" % (count, word))
                try:
                    result = fetch_osd_page(word)
                except Exception:
                    result = None
                
                if result == None:
                    errfile.write(word + "\n")
                    sys.stderr.write(" ! Error on word %d, %s...\n" % (count, word))
                else:
                    for defn in result:
                        g.write("|||".join(defn).encode("utf-8") + "\n")
                if count % 10 == 0:
                    sys.stderr.write(" * Sleeping ...\n")
                    time.sleep(2)

if __name__ == "__main__":
   # [Input file name] [output file name] [error log file]
   #print fetch_osd_page('5150ed someone')
   if len(sys.argv) < 4:
       print "onlineslangdict.pages [input word list] [output file] [error log file]"
       exit(1)
   with open(sys.argv[3], 'w') as f:
       fetch_all_pages(sys.argv[1], sys.argv[2], f)



