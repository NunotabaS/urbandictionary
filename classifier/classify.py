import sys
import re
from sklearn import linear_model, datasets

FEATURES_VECTOR_LABEL = []

def split_words(sent):
  return re.split(r"[^a-zA-Z0-9-]", sent)

def generate_features(definition, votes):
  words = [w.lower() for w in split_words(definition)]
  upvotes, downvotes = tuple(votes.split(',')) 
  upvotes = int(upvotes) if upvotes.strip() != "" else 0
  downvotes = int(downvotes) if downvotes.strip() != "" else 0
  feat = [upvotes, downvotes]
  for w in FEATURES_VECTOR_LABEL:
    feat.append(sum(1 if w == k else 0 for k in words))
  return feat

# Populates the features vector label
WORDS = set()
with open(sys.argv[1],'r') as f:
  for line in f:
    label, word, sent, ex, voting = tuple(line.strip().split("|||"))
    words = [w.lower() for w in split_words(sent)]
    for word in words:
      WORDS.add(word)

for w in WORDS:
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


