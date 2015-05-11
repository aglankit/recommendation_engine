#1.129
import pandas as pd
import numpy as np
import sys
import csv

languages = []
input = sys.argv[1]
ftr = open(input, "rb")

reader = csv.DictReader(ftr)
for row in reader:
  item = "%s" % (row['Languages'])
  languages.append(item)

#print pd.Series(languages).str.get_dummies()
#print languages

ftr.close()
