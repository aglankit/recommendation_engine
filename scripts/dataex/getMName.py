import csv
import sys
import arff

inFile = sys.argv[1]
field = sys.argv[2]
fp = open(inFile, "rb")

reader = csv.DictReader(fp, delimiter='|')

for row in reader:
  print row[field]
