#1.129
import pandas as pd
import numpy as np
import sys
import csv


pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100000)
pd.set_option('expand_frame_repr', False)

languages = []
train = sys.argv[1]
ftr = open(train, "rb")

reader = csv.DictReader(ftr)
for row in reader:
  item = "%s" % (row['Languages'])
  languages.append(item)

df = pd.DataFrame(languages, columns=['Languages'])

print pd.get_dummies(df['Languages'])
