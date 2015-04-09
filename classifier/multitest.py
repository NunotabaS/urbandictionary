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
  upvotes = int(re.sub(r"[^0-9-]","",upvotes)) if upvotes.strip() != "" else 0
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
    label, word, sent, ex, voting = tuple(line.strip().split("|||"))
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
training_answers  = [1 if tup[0] == "g" else -1 for tup in train]

DATA_LENGTH = len(train)

TP, FP, TN, FN = 0, 0, 0, 0

for r in xrange(0, 5):
  sys.stderr.write("Round %i\r" % r)
  test_pairs = training_pairs[(DATA_LENGTH / 5) * r:(DATA_LENGTH / 5) * (r + 1)]
  test_answers = training_answers[(DATA_LENGTH / 5) * r:(DATA_LENGTH / 5) * (r + 1)]
  
  train_pairs = training_pairs[0:(DATA_LENGTH / 5) * r] + training_pairs[(DATA_LENGTH / 5) * (r+1):]
  train_answers = training_answers[0:(DATA_LENGTH / 5) * r] + training_answers[(DATA_LENGTH / 5) * (r+1):]
  
  print "Train size: %i" % len(train_pairs)
  
  logreg = linear_model.LogisticRegression(C=1e5)
  logreg.fit(train_pairs, train_answers)
  tp, fp, tn, fn = 0, 0, 0, 0
  for (feat, lab) in zip(test_pairs, test_answers):
    label = 'g' if logreg.predict(feat) > 0 else 'n'
    answer = 'g' if lab > 0 else 'n'
    if answer == 'g':
      if label == 'g':
        tp += 1
      else:
        fn += 1
    else:
      if label == 'g':
        fp += 1
      else:
        tn += 1
  print (tp, fp, tn, fn)
  precision, recall = float(tp) / (tp + fp), float(tp) / (fn + tp)
  print "Current round precision: %f, Recall: %f" % (precision, recall)
  
  TP += tp
  FP += fp
  TN += tn
  FN += fn
  
precision, recall = float(tp) / (tp + fp), float(tp) / (fn + tp)
fscore = 2 * (precision * recall) / (precision + recall)
print "Precision: %f, Recall: %f, FScore: %f" % (precision, recall, fscore)


