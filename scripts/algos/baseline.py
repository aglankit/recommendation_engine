import csv
import sys
import numpy as np
import warnings
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def getUserAverage(user):
  list = []
  for column in range(0,1682):
    if Utility[user][column] > 0:
      list.append(Utility[user][column])
  try:
    result = np.average(list) - av
  except Warning:
    result = 0.0  
  return result

def getItemAverage(item):
  list = []
  for row in range(0, 943):
    if Utility[row][item] > 0:
      list.append(Utility[row][item])
  try:
    result = np.average(list) - av 
  except Warning:
    result = 0.0
  return result

def getOverallAverage():
  global av
  list = []
  for i in range(max_users):
    for j in range(max_items):
      if Utility[i][j] > 0:
        list.append(Utility[i][j])
  av = np.average(list)

train = sys.argv[1]
ftr = open(train, "rb")

test = sys.argv[2]
fte = open(test, "rb")

warnings.filterwarnings('error')

max_items = 1682
max_users = 943
av = 0.0
av_users = np.array([0 for x in range(max_users)], dtype=float)
av_items = np.array([0 for x in range(max_items)], dtype=float)
Utility = [[0 for x in range(1682)] for x in range(943)]

reader = csv.DictReader(ftr, delimiter='\t')
for row in reader:
  Utility[int(row['uid'])-1][int(row['mid'])-1] = int(row['rating'])

getOverallAverage()

for user in range(max_users):
  av_users[user] = getUserAverage(user)

for item in range(max_items):
  av_items[item] = getItemAverage(item)

y_true = []
y_pred = []

reader = csv.DictReader(fte, delimiter='\t')
for row in reader:
  y_true.append(int(row['rating']))
  #y_pred.append(av)
  y_pred.append(av + av_users[int(row['uid'])-1] + av_items[int(row['mid'])-1])

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
