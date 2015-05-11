import csv
import sys
import numpy as np
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def getReviewsSet(row):
  global max_items
  list = Set()
  for column in range(0,max_items):
    if Utility[row][column] > 0:
      list.add(column)
  return list

def getReview(user):
  global max_items
  list = []
  for column in range(0,max_items):
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
  global max_users
  for row in range(0, max_users):
    for column in range(row + 1, max_users):
      sim = calculateSimilarityUsers(row, column);
      Similarity[row][column] = sim
      Similarity[column][row] = sim

def fillAverageMatrix():
  global Average
  global max_users
  for user in range(0, max_users):
    Average[user] = np.average(getReview(user))

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
  global max_users
  users = []
  weight = []
    
  reset_topn()
  for rater in range(0, max_users):
    if Utility[rater][item] > 0:
      maintain_topn(Similarity[user][rater], Utility[rater][item])

    for entry in topn:
      weight.append(entry[0])
      users.append(entry[1])

  return (np.average(users, weights = weight))

train = sys.argv[1]
ftr = open(train, "rb")

test = sys.argv[2]
fte = open(test, "rb")

max_items = 1682
max_users = 943
topn =[]
n = int(sys.argv[3])

Average = np.array([0 for x in range(max_users)], dtype=float)
Utility = [[0 for x in range(max_items)] for x in range(max_users)] 
Similarity = np.array([[0 for x in range(max_users)] for x in range(max_users)], dtype=float)

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

#print len(y_pred)
#print len(y_true)
#print topn

fte.close()
ftr.close()

#print ("%d Nearest neighbor (Users) ---" % n)
print ("Mean Absolute Error is %f") % (mean_absolute_error(y_true, y_pred))
print ("Mean Squared Error is %f") % (mean_squared_error(y_true, y_pred))

accurate = 0;
result = np.asarray(y_true)
pred = np.asarray(y_pred)
for i in range(len(pred)):
  if (int(result[i]) == int(round(pred[i]))):
    accurate = accurate + 1

print ("Accuracy is: %f") % (round(accurate)/len(y_pred))
