'''
Visualize missing values by plotting the matrix
'''

import csv
import numpy as np
import pylab as pl
from datools.maptrix import Maptrix, align_array
from scipy.misc import imsave

csv_link = '/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_year_cty.csv'
data_file = csv.reader(open(csv_link, 'r'), delimiter=',', quotechar='"')
data = []
header = data_file.next()
countries = []
years = []
for line in data_file:
    year, cty, name, line = line[0], line[1], line[2] ,line[3:]
    years.append(year)
    countries.append(cty)
    for j in range(len(line)):
        try:
            line[j] = float(line[j])
            line[j] = 1000
        except:
            line[j] = 0
    data.append(line)
years = list(set(years))
countries = list(set(countries))

data_yc = np.array(data)
print 'Created data_yc'
data_cy = np.zeros(data_yc.shape)
nc = len(countries)
ny = len(years)
for year in range(len(years)):
    for cty in range(len(countries)):
        data_cy[cty*ny + year] = data_yc[year*nc + cty]
print 'Created data_yc'

#m_yc = Maptrix(data_yc).savefig('/home/dani/AAA/LargeData/WDlandGDF_processed/m_yc.png')
#im = imsave('/home/dani/AAA/LargeData/WDlandGDF_processed/m_yc.png', align_array(data_yc))
#im = imsave('/home/dani/AAA/LargeData/WDlandGDF_processed/m_cy.png', align_array(data_cy))
print 'Created maptrix'
