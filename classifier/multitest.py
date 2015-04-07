import sys
import re
from nltk.stem import porter
from sklearn import linear_model, datasets

FEATURES_VECTOR_LABEL = []
FEATURE_CUTOFF = 0
USE_STEM = False

porterstemmer = porter.PorterStemmer()
def split_words(sent):
  return [porterstemmer.stem(word.lower()) if USE_STEM else word.lower() for word in re.split(r"[^a-zA-Z0-9-]", sent) if word.strip() != ""]

def bigrams(words):
  return [(words[i], words[i+1]) for i in xrange(0,len(words) - 1)]

def generate_features(definition, votes):
  words = split_words(definition)
  bigram_words = bigrams(words)
  upvotes, downvotes = tuple(votes.split(',')) 
  upvotes = int(upvotes) if upvotes.strip() != "" else 0
  downvotes = int(downvotes) if downvotes.strip() != "" else 0
  ratio = float(upvotes) / (upvotes + downvotes) if (upvotes + downvotes) > 0 else 0
  #feat = [ratio, 1 - ratio, upvotes, downvotes]# 1 if definition.strip()[-1] == "." else 0]
  feat = []
  for w in FEATURES_VECTOR_LABEL:
    feat.append(1 if any(w == k for k in words) else 0) # + (1 if any(w == k for k in bigram_words)) 
    #feat.append(sum(1 if w == k else 0 for k in words) + sum(1 if w==k else 0 for k in bigram_words))
  return feat

# Populates the features vector label
WORDS = {}
with open(sys.argv[1],'r') as f:
  for line in f:
    _, label, word, sent, ex, voting = tuple(line.strip().split("|||"))
    words = [w.lower() for w in split_words(sent)]
    #words += bigrams(words)
    for word in words:
      if word in WORDS:
        WORDS[word] += 1
      else:
        WORDS[word] = 1

for w in WORDS:
  if WORDS[w] > FEATURE_CUTOFF:
    FEATURES_VECTOR_LABEL.append(w)
    

train = [tuple(line.strip().split('|||')) for line in open(sys.argv[1])]
training_pairs  = [generate_features(tup[2], tup[4]) for tup in train]
training_answers  = [1 if tup[0] == "g" else 0 for tup in train]

logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(training_pairs, training_answers)

with open(sys.argv[2],'r') as f:
  for line in f:
    word, defn, ex, voting = tuple(line.strip().split("|||"))
    print "|||".join(('g' if logreg.predict(generate_features(defn, voting)) > 0 else 'n', word, defn, ex, voting))


