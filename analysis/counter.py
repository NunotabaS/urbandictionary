import re

words, phrases, emotes = 0, 0, 0
with open("../scraper/dict.tsv","r") as f:
  for line in f:
    if re.match(r"^[^a-zA-Z0-9]*$", line.strip()) != None:
      emotes += 1
      continue
    if " " in line.strip():
      phrases += 1
    else:
      words += 1

print "Words: %i, Phrases: %i, Emoji: %i" % (words, phrases, emotes)
