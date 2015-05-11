#1.129
import pandas as pd
import numpy as np
import sys
import csv

#df = pd.DataFrame(['Slow', 'Normal', 'Fast', 'Fast|Slow', 'Slow'], columns=['Speed'])
#print df

#print pd.get_dummies(df['Speed'])

directors = []
train = sys.argv[1]
ftr = open(train, "rb")

reader = csv.DictReader(ftr, delimiter='|')
for row in reader:
  item = "%s|%s" % (row['actor1'], row['actor2'])
  directors.append(item)

#print pd.Series(["Slow|Fast||", np.nan, "Slow||Med"]).str.get_dummies()
print pd.Series(directors).str.get_dummies()
print directors

ftr.close()
