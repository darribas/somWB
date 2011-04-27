import pysal as ps
link = '/Users/dani/AAA/LargeData/WDIandGDF_csv/WDI_GDF_Series.csv'
csv = ps.open(link)

def printD(d):
    for i in d:
        print '%s\tvars in topic %s'%(str(d[i]), i)
    print 'Total vars: %i'%sum([d[i] for i in d])

topics = {}

for i in csv:
    if i[-6] in topics:
        topics[i[-6]] += 1
    else:
        topics[i[-6]] = 1

printD(topics)

