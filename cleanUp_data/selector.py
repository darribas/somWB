'''
Print basic stats and select data for the SOM
'''

import pylab as pl
from datools.maptrix import Maptrix, align_array
from scipy.misc import imsave

csv_link = '/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_year_cty.csv'
data_file = csv.reader(open(csv_link, 'r'), delimiter=',', quotechar='"')
data = []
header = data_file.next()
countries = []
years = []
ydata = {}
cdata = {}
vdata = {}
empties = {}
for line in data_file:
    year, cty, name, line = line[0], line[1], line[2] ,line[3:]
    years.append(year)
    countries.append(cty)
    empty = True
    for j in range(len(line)):
        try:
            line[j] = float(line[j])
            line[j] = 1000
            empty = False
        except:
            line[j] = 0
        if j in vdata:
            vdata[j].append(line[j])
        else:
            vdata[j] = [line[j]]
        if year in ydata:
            ydata[year].append(line[j])
        else:
            ydata[year] = [line[j]]
        if cty in cdata:
            cdata[cty].append(line[j])
        else:
            cdata[cty] = [line[j]]
    if empty:
        #print '%s\t%s\t%s'%(year, cty, name)
        if name in empties:
            empties[name].append(year)
        else:
            empties[name] = [year]
    data.append(line)

for cty in empties:
    #print cty, empties[cty]
    pass

pct_var = {}
for var in vdata:
    pct_var[var] = len([i for i in vdata[var] if i == 1000]) / float(len([i for i in vdata[var]]))

for var in range(len(vdata.keys())):
    print 'Var: %s\tPct: %.3f'%(var, pct_var[var])


pct_year = {}
for year in ydata:
    pct_year[year] = len([i for i in ydata[year] if i == 1000]) / float(len([i for i in ydata[year]]))

for year in set(years):
    print 'Year: %s\tPct: %.3f'%(year, pct_year[year])

pct_cty = {}
for cty in cdata:
    pct_cty[cty] = len([i for i in cdata[cty] if i == 1000]) / float(len([i for i in cdata[cty]]))

for cty in countries:
    print 'Country: %s\tPct: %.3f'%(cty, pct_cty[cty])


