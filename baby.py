import csv
import sys
import os

# os.chdir('dataset/LLDOS-1')

# for name in os.listdir("."):
#     print name 

f = open('dataset/LLDOS-1/dmzphase1.csv', 'rb')

reader = csv.reader(f)
for row in reader:
    alert = row[1:],'dmzphase1'
    print alert

# for x in range(len(alerts)):
#     print alerts[x]

f.close()