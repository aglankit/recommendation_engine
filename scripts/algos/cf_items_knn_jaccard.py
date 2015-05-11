import csv
import sys
import warnings
import numpy as np
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import jaccard_similarity_score


def getReview(item):
  global max_users
  list = []
  for column in range(0, max_users):
    if Utility[item][column] > 0:
      list.append(Utility[item][column])
  return list


def calculateSimilarityItems(item1, item2):
  try:
    result = jaccard_similarity_score(Utility[item1], Utility[item2])
  except Warning:
    #print "Exception at %d : %d" % (item1, item2)
    result = 0.5
  return result

def fillSimilarityMatrix():
  global Similarity
  global max_items
  for row in range(0, max_items):
    for column in range(row + 1, max_items):
      sim = calculateSimilarityItems(row, column);
      Similarity[row][column] = sim
      Similarity[column][row] = sim

def fillAverageMatrix():
  global Average
  global max_items
  for item in range(0, max_items):
    try:
      Average[item] = np.average(getReview(item))
    except Warning:
      Average[item] = 3.0
    #print getReview(user)
    #print Average[user]

def reset_topn():
    global topn
    global n
    topn =[(0.0, 0) for x in range(n)]

def maintain_topn(similar, user):
    global topn
    topn.append((similar, user))
    topn = sorted(topn, key=lambda x: x[0], reverse=True)
    topn.pop()

def predictRating(user, item):
  global topn
  global max_items
  items = []
  weight = []

  reset_topn()
  for rated_item in range(0, max_items):
    if Utility[rated_item][user] > 0:
      maintain_topn(Similarity[item][rated_item], Utility[rated_item][user])

    for entry in topn:
      weight.append(entry[0])
      items.append(entry[1])

  return (np.average(items, weights = weight))


train = sys.argv[1]
ftr = open(train, "rb")

test = sys.argv[2]
fte = open(test, "rb")

warnings.filterwarnings('error')

max_items = 1682
max_users = 943
topn =[]                                            
n = int(sys.argv[3])

Utility = [[0 for x in range(max_users)] for x in range(max_items)]
Similarity = np.array([[0 for x in range(max_items)] for x in range(max_items)], dtype=float)
Average = np.array([0 for x in range(max_items)], dtype=float)

reader = csv.DictReader(ftr, delimiter='\t')
for row in reader:
  Utility[int(row['mid'])-1][int(row['uid'])-1] = int(row['rating'])

fillSimilarityMatrix()
fillAverageMatrix()

y_true = []
y_pred = []

reader = csv.DictReader(fte, delimiter='\t')
for row in reader:
  rating = 0.0
  y_true.append(int(row['rating']))
  try:
    rating = predictRating(int(row['uid'])-1, int(row['mid'])-1)
    y_pred.append(rating)
  except:
    rating = Average[int(row['mid'])-1]
    if rating == 0.0:
      print "Rating = 0 for %d" % int(row['mid'])
      rating = 3.0
    y_pred.append(rating)

#print y_pred
#print y_true
#print len(y_pred)
#print len(y_true)

fte.close()
ftr.close()

print ("Mean Absolute Error is %f") % (mean_absolute_error(y_true, y_pred))
print ("Mean Squared Error is %f") % (mean_squared_error(y_true, y_pred))

accurate = 0;
result = np.asarray(y_true)
pred = np.asarray(y_pred)
for i in range(len(pred)):
  if (int(result[i]) == int(round(pred[i]))):
    accurate = accurate + 1

print ("Accuracy is: %f") % (round(accurate)/len(y_pred))
