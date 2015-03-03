import sys, re
from nltk.stem import porter # use the porter stemmer here

def wordmodify(word):
    # fix multi-repeats
    return word

def getdict(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield wordmodify(line.decode("utf8").strip().lower())

def getstem(wdict):
    porterstemmer = porter.PorterStemmer()
    for word in wdict:
        yield porterstemmer.stem(word)

def getstemmap(wdict):
    # do something
    porterstemmer = porter.PorterStemmer()
    stemdict = {}
    for word in wdict:
        stemmed = porterstemmer.stem(word)
        if stemmed in stemdict:
            stemdict[stemmed].append(word)
        else:
            stemdict[stemmed] = [word]
    return stemdict

if __name__ == '__main__':
    # params [urban dictionary file] [onlineslang dictionary file] [match mode]
    if(len(sys.argv) < 4 or sys.argv[3] != 'stem'):
        udset, osdset = set(getdict(sys.argv[1])), set(getdict(sys.argv[2]))
        for word in udset.intersection(osdset):
            print word
    else:
        stemmap = getstemmap(getdict(sys.argv[1]))
        st_udset, st_osdset = set(getstem(getdict(sys.argv[1]))), set(getstem(getdict(sys.argv[2])))
        for st_word in st_udset.intersection(st_osdset):
            for orig in stemmap[st_word]:
                print orig
