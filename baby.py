import csv
import sys

f = open(sys.argv[1], 'rt')
d = open(sys.argv[2], 'rt')
try:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if i!=1:
            i++
            continue
        print row

    reader = csv.reader(d)
    i = 0
    for row in reader:
        if i!=1:
            i++
            continue
        print row
finally:
    f.close()