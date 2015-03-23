import sys, re

def getdefs(filename, skip = 0):
    with open(filename, 'r') as f:
        for line in f:
            if skip > 0:
                skip -= 1;
                continue;
            yield tuple(line.decode("utf8").strip().split("|||"))

if __name__ == '__main__':
    for kbdata in getdefs(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0):
        print "====================="
        print "Word: " + kbdata[0]
        print "Definition: "
        print kbdata[1]
        print ""
        print "Example:" + kbdata[2]
        print ""
        print kbdata[3]
        print "===================="
        cname = raw_input('Press any key to continue...')
