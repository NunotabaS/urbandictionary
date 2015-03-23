import sys, re

def wordmodify(word):
    return word
    
def getdict(filename, lc = None):
    with open(filename, 'r') as f:
        l = 0
        for line in f:
            l += 1
            if lc != None:
                if l > lc:
                    return
            yield wordmodify(line.decode("utf8").strip().lower())

def getdefs(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield tuple(line.decode("utf8").strip().split("|||"))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "extractdefinitions [defns file] [word list] [word limit] [anti-list]"
        exit(1)
    
    if(len(sys.argv) >= 3):
        wlset =  set(getdict(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].lower() != 'none' else None))
        for defn in getdefs(sys.argv[1]):
            isAntilist = True if len(sys.argv) > 4 and sys.argv[4] == 'anti' else False
            if not isAntilist:
                if defn[0].strip().lower() in wlset:
                    print "|||".join(defn).encode("utf8")
            else:
                if not defn[0].strip().lower() in wlset:
                    print "|||".join(defn).encode("utf8")
