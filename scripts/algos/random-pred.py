import csv
import sys
import random
import numpy as np
from sets import Set
from scipy import spatial
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

test = sys.argv[2]
fte = open(test, "rb")

max_items = 1682
max_users = 943

y_true = []
y_pred = []

reader = csv.DictReader(fte, delimiter='\t')
for row in reader:
  y_true.append(int(row['rating']))
  y_pred.append(random.randint(1,5))

fte.close()

print ("Mean Absolute Error is %f") % (mean_absolute_error(y_true, y_pred))
print ("Mean Squared Error is %f") % (mean_squared_error(y_true, y_pred))

#print y_pred

accurate = 0;
result = np.asarray(y_true)
pred = np.asarray(y_pred)
for i in range(len(pred)):
  if (int(result[i]) == int(round(pred[i]))):
    accurate = accurate + 1

print ("Accuracy is: %f") % (round(accurate)/len(y_pred))
