import sys, re
from nltk.stem import porter # use the porter stemmer here

def wordmodify(word):
    # fix multi-repeats
    return word

def getdict(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield wordmodify(line.strip().lower())
def getstem(wdict):
    # do something
    return wdict

if __name__ == '__main__':
    udset, osdset = set(getdict(sys.argv[1])), set(getdict(sys.argv[2]))
    for word in udset.intersection(osdset):
        print word
