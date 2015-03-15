import sys, re
from nltk.stem import porter # use the porter stemmer here

def wordmodify(word):
    # fix multi-repeats
    return word

def getdict(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield wordmodify(line.decode("utf8").strip().lower())

if __name__ == '__main__':
    # params [binfile] [onlineslang dictionary file]
    binset, osdset = set(getdict(sys.argv[1])), set(getdict(sys.argv[2]))
    for word in osdset.difference(binset):
        print word
