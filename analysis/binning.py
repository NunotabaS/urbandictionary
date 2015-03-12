import sys, re
from nltk.stem import porter # use the porter stemmer here

def generatebins(filename):
    table = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == "":
                continue;
            word, bin, grammatical_comp, defintion = tuple(line.strip().split("|||"))
            table[word.lower()] = bin.strip().lower()
    return table

def wordmodify(word):
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
    if len(sys.argv) < 3:
        print "binning [matchwords file] [onlineslang dictionary definitions file]"
        exit(1)
    table = generatebins(sys.argv[2])
    bins = set()
    for word in getdict(sys.argv[1]):
        bins.add(table[word])
    for binid in bins:
        print binid

