import csv
import sys
import numpy as np
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def getReviewsSet(row):
  list = Set()
  for column in range(0,1682):
    if Utility[row][column] > 0:
      list.add(column)
  return list

def getReview(user):
  list = []
  for column in range(0,1682):
    if Utility[user][column] > 0:
      list.append(Utility[user][column])
  return list

def calculateSimilarityUsers(user1, user2):
  result = 1 - spatial.distance.cosine(Utility[user1], Utility[user2])
  return result

def calculateSimilarityItems(item1, item2):
  result = 1 - spatial.distance.cosine(Utility[item1], Utility[item2])
  return result

def fillSimilarityMatrix():
  global Similarity
  for row in range(0, 943):
    for column in range(row + 1, 943):
      sim = calculateSimilarityUsers(row, column);
      Similarity[row][column] = sim
      Similarity[column][row] = sim

def fillAverageMatrix():
  global Average
  for user in range(0, 943):
    Average[user] = np.average(getReview(user))
    #print getReview(user)
    #print Average[user]

def predictRating(user, item):
  users = []
  weight = []
  for rater in range(0, 943):
    if Utility[rater][item] > 0:
      users.append(Utility[rater][item])
      weight.append(Similarity[user][rater])
      #print "%d, %f" % (Utility[rater][item], Similarity[user][rater])
  return (np.average(users, weights = weight))

train = sys.argv[1]
ftr = open(train, "rb")

test = sys.argv[2]
fte = open(test, "rb")

max_items = 1682
max_users = 943

Average = np.array([0 for x in range(943)], dtype=float)
Utility = [[0 for x in range(1682)] for x in range(943)] 
Similarity = np.array([[0 for x in range(943)] for x in range(943)], dtype=float)

reader = csv.DictReader(ftr, delimiter='\t')
for row in reader:
  Utility[int(row['uid'])-1][int(row['mid'])-1] = int(row['rating'])

fillAverageMatrix()
fillSimilarityMatrix()

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
