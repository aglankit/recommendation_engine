import csv
import sys
import numpy as np
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


def getReview(item):
  global max_users
  list = []
  for column in range(0, max_users):
    if Utility[item][column] > 0:
      list.append(Utility[item][column])
  return list


def calculateSimilarityItems(item1, item2):
  result = 1 - spatial.distance.cosine(Utility[item1], Utility[item2])
  return result

def fillSimilarityMatrix():
  global max_items
  for row in range(0, max_items):
    for column in range(row + 1, max_items):
      sim = calculateSimilarityItems(row, column);
      Similarity[row][column] = sim
      Similarity[column][row] = sim

def fillAverageMatrix():
  global max_items
  for item in range(0, max_items):
    Average[item] = np.average(getReview(item))
    #print getReview(user)
    #print Average[user]

def predictRating(user, item):
  global max_items
  items = []
  weight = []
  for reted_item in range(0, max_items):
    if Utility[rated_item][user] > 0:
      items.append(Utility[rated_item][user])
      weight.append(Similarity[rated_item][user])
      #print "%d, %f" % (Utility[rater][item], Similarity[user][rater])
  return (np.average(items, weights = weight))


train = sys.argv[1]
ftr = open(train, "rb")

test = sys.argv[2]
fte = open(test, "rb")

max_items = 1682
max_users = 943

Utility = [[0 for x in range(max_users)] for x in range(max_items)]
Similarity = np.array([[0 for x in range(max_items)] for x in range(max_items)], dtype=float)
Average = np.array([0 for x in range(max_items)], dtype=float)

reader = csv.DictReader(ftr, delimiter='\t')
for row in reader:
  Utility[int(row['uid'])-1][int(row['mid'])-1] = int(row['ratings'])
ftr.close()

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
    rating = Average[int(row['uid'])-1]
    y_pred.append(rating)

print y_pred
print y_true
print len(y_pred)
print len(y_true)

fte.close()

#print ("Mean absolute error is %f; Root Mean Squared Error is %f") % (mean_absolute_error(y_true, y_pred), mean_squared_error(y_true, y_pred))
print ("Root Mean Squared Error is %f") % (mean_squared_error(y_true, y_pred))
