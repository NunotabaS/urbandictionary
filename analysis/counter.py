import re, sys

words, phrases, emotes = 0, 0, 0
nphrases = [0] * 16

if len(sys.argv) < 2:
    print "counter [word list]"
    exit(1)

with open(sys.argv[1],"r") as f:
  for line in f:
    if re.match(r"^[^a-zA-Z0-9]*$", line.strip()) != None:
      emotes += 1
      continue
    if len(line.strip()) == 0:
      continue
    if " " in line.strip():
      swords = line.strip().split(" ")
      if len(swords) == 1:
        print swords
      
      wc = len(swords)
      nphrases[wc - 1 if wc < 15 else 15] += 1
      phrases += 1
    else:
      words += 1

print "Words: %i, Phrases: %i, Emoji: %i" % (words, phrases, emotes)
nphrases[0] = words
print nphrases
print sum(nphrases)
