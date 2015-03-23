import sys, re

def getdefs(filename, skip = 0):
    with open(filename, 'r') as f:
        for line in f:
            if skip > 0:
                skip -= 1;
                continue;
            yield tuple(line.decode("utf8").strip().split("|||"))

if __name__ == '__main__':
    with open(sys.argv[2], "a") as f:
        for kbdata in getdefs(sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 else 0):
            print "Word: " + kbdata[0]
            print "Definition: "
            print kbdata[1]
            print ""
            print "Example:" + kbdata[2]
            print ""
            print kbdata[3]
            print "===================="
            good = raw_input('Good record or not (g/n) : ')
            print ""
            #+ wsense + "|||"
            f.write(good + "|||" + "|||".join(kbdata).encode("utf8") + "\n");
