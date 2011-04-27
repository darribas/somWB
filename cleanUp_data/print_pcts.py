'''
Print precentages of not missing values in variables
'''

data_link = '/Users/dani/AAA/LargeData/WDlandGDF_processed/wbALL_no_empties.dat'

data = open(data_link)
h, n = data.readline(), data.readline()
h = h.strip('\n').split(' ')
vars = {} #vars[name] = n
total = 0
for var in h:
    vars[var] = 0
for line in data:
    line = line.strip('\n').split(' ')
    for var in range(len(line)):
        try:
            line[var] = float(line[var])
            vars[h[var]] += 1
        except:
            vars[h[var]] += 0
        total += 1
data.close()
total_var = float(total) / (len(h) - 1)
for var in range(len(vars)):
    print '%f\tpct for var %s'%(vars[h[var]]/total_var, h[var])
