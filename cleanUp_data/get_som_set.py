'''
Pull out countries with at least one completely empty row and write
them out in .dat format
'''

import csv
import numpy as np
from datools.som import stdDat

csv_link = '/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_year_cty.csv'
data_file = csv.reader(open(csv_link, 'r'), delimiter=',', quotechar='"')
header = data_file.next()
header = [i.replace(' ', '') for i in header]

dat_link = '/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_no_empties.dat'
fo = open(dat_link, 'w')
h = '# '
h += ' '.join(header[3:])
h += ' '
h += '-'.join(header[:3])
h += '\n'
fo.write(h)
fo.write('%i\n'%len(header[3:]))

countries = []
years = []
empties = []
data = []
for line in data_file:
    year, cty, name, line = line[0], line[1], line[2] ,line[3:]
    years.append(year)
    countries.append(cty)
    empty = True
    for j in range(len(line)):
        try:
            check = float(line[j])
            empty = False
        except:
            line[j] = 'x'
    if empty:
        empties.append(cty)
    meta = '_'.join([year, cty, name.replace(' ', '_')])
    line.append(meta)
    data.append(line)
empties = list(set(empties))
print empties
for line in data:
    if line[-2] not in empties:
        line = map(str, line)
        line = ' '.join(line)
        line += '\n'
        fo.write(line)
fo.close()

stdDat(dat_link[:-4])

