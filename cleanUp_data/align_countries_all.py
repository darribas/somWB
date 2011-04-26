'''
Organize raw data on .dat format to run first SOM and have something to play
with
'''

import csv

raw_csv = '/home/dani/AAA/LargeData/WDIandGDF_csv/WDI_GDF_Data.csv'

data = {} # data[cty][year] = {'var_names': [], 'var_values': []

csv = csv.reader(open(raw_csv, 'r'), delimiter = ',', quotechar='"')
years = csv.next()[4:]

variables = []
countries = []
cty2name = {}

for line in csv:
    var, var_name, cty, cty_name, values = line[0], line[1], line[2], line[3], \
            line[4:]
    variables.append(var)
    countries.append(cty)
    if cty not in cty2name:
        cty2name[cty] = cty_name
    if cty not in data:
        data[cty] = {}
    for year in years:
        if year not in data[cty]:
            data[cty][year] = {}
        data[cty][year][var] = values[years.index(year)]

variables = list(set(variables))
variables.sort()
countries = list(set(countries))
countries.sort()

print 'Data loaded'

fo = open('/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_year_cty.csv', 'w')
header = 'year,country,country_name,'
vars = ','.join(variables)
header += vars
header += '\n'
fo.write(header)
for year in years:
    print 'Writing year %s'%year
    for cty in countries:
        line = '%s,"%s","%s"'%(year, cty, cty2name[cty])
        for var in variables:
            if var in data[cty][year]:
                line += ',%s'%data[cty][year][var]
            else:
                line += ','
        line += '\n'
        fo.write(line)
fo.close()

