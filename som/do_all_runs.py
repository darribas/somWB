"""Script to do all the new runs"""
from runSom import bestMap

somPakF='/home/dani/repos/som_pak-3.1/'

data = '/home/dani/AAA/LargeData/WDlandGDF_processed/wbALL_no_emptiesZ.dat'

runs = 1

Run=1
datIn = data
cols,rows,topo,neigh=map(str,[1500, 1500,'hexa','gaussian'])
rlen1,alpha1,radious1=map(str,[10000,0.04,750])
rlen2,alpha2,radious2=map(str,[100000,0.03,500])
nameO='/home/dani/AAA/LargeData/WDlandGDF_processed/som1'

bestMap(runs, somPakF,datIn,cols,rows,topo,neigh,rlen1,alpha1,radious1,rlen2,alpha2,radious2,nameO)
print 'Run %i done'%Run
print '###################################################'

