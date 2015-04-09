import sys
import re
import random

with open(sys.argv[1],'r') as f:
  for line in f:
    _, word, defn, ex, voting = tuple(line.strip().split("|||"))
    print "|||".join(('g' if random.random() > 0.5 else 'n', word, defn, ex, voting))
