"""
======================================================================
Python Self-Organizing Maps -- Data Tools and utilities
----------------------------------------------------------------------
AUTHOR(S):      Charles R. Schmidt cschmidt@rohan.sdsu.edu
                Dani Arribas-Bel daniel.arribas.bel@gmail.com
======================================================================
"""

from math import sqrt
import pysal, os, time, copy
from math import sin,cos,pi
import commands as cmds

def hexPts(cols,rows):
    """ Draw the pts for a hex topology, modified from Martin's CODtoSHP.py """
    #modified
    y = rows
    x = cols
    #
    deltaX = 1.0
    deltaY = sqrt(3.0/4.0)
    hexX=0-deltaX
    hexY=0
    pts = []
    for lcvY in range(y):
        for lcvX in range(x):
            hexX+=deltaX
            pts.append([hexX,hexY])
        if (lcvY+1)%2:
            hexX=0-(deltaX/2)
        else:
            hexX=0-deltaX
        hexY=hexY+deltaY
    return pts

def hexPtsBmus(cols,rows):
    """ Draw the pts for a hex topology, modified from Martin's CODtoSHP.py """
    x = rows
    y = cols
    deltaX = 1.0
    deltaY = sqrt(3.0/4.0)
    hexX=0-deltaX
    hexY=0
    pts = {}
    for lcvY in range(y):
        for lcvX in range(x):
            hexX+=deltaX
            pts[(lcvX,lcvY)]=[hexX,hexY]
        if (lcvY+1)%2:
            hexX=0-(deltaX/2)
        else:
            hexX=0-deltaX
        hexY=hexY+deltaY
    return pts

def rookPoly(pts):
    """ Draw the polygons for a rook topology """
    deltaX = 1.0
    deltaY = 1.0
    centroidsDist = 1.0
    polygons = []
    for i in pts:
        pX = i[0]
        pY = i[1]
        poly =[ 0,
                [(pX-(deltaX/2),pY+(deltaY/2)), 
                (pX+(deltaX/2),pY+(deltaY/2)),
                (pX+(deltaX/2),pY-(deltaY/2)),
                (pX-(deltaX/2),pY-(deltaY/2)),
                (pX-(deltaX/2),pY+(deltaY/2)) ]]
        polygons.append(poly)
    return polygons
def hexPoly(pts):
    """ Draw the polygons for a hex topology, modified from Martin's CODtoSHP.py """
    deltaX = 1.0
    deltaY = sqrt(3.0/4.0)
    centroidsDist = 1.0
    polygons = []
    for i in pts:
        #center point
        pX=i[0]
        pY=i[1]
        #sides numberd in order of min length
        side2=0.5*centroidsDist
        side1=side2/sqrt(3)
        side3=2*side1
        #derive extreama
        minX=pX-side2
        maxX=pX+side2
        minY=pY-side3
        maxY=pY+side3
        #bounding box
        Box=[minX,minY,maxX,maxY]
        #number of parts
        NumParts=1
        #number of points
        NumPoints=6
        #index to first point in part
        Parts=0
        #starts from top most, left most, and goes clock-wise        
        Points=[Box,[[pX,pY+side3],[pX+side2,pY+side1],[pX+side2,pY-side1],[pX,pY-side3],[pX-side2,pY-side1],[pX-side2,pY+side1]]]
        polygons.append(Points)
    return polygons
def writePoly(fName,polys):
    f = open(fName,'w')
    f.write('POLYGON\n')
    for i,poly in enumerate(polys):
        f.write('%d 0\n'%(i))
        poly = poly[1]
        poly = ['%d %f %f\n'%(i,pt[0],pt[1]) for i,pt in enumerate(poly)]
        f.writelines(poly)
        f.write('%d'%(i+1)+poly[0][1:]) #close the loop
    f.write('END\n')
    f.close()

def getHexShp(codeBook,outFile):
    """Create the hexagon shapeFile
    Do NOT specify file extension in outFile"""
    inCOD = open(codeBook)
    inCOD = inCOD.readlines()
    header = inCOD.pop(0)
    dims,topo,cols,rows,neigh = header.split()
    cols=int(cols)
    rows=int(rows)
    fieldSpec = [('N',20,10)]*int(dims)
    fieldHead = ['plane%d'%i for i in range(int(dims))]
    #hexpts=hexPts(x,y) #Orig WRONG!!!
    hexpts=hexPts(cols,rows)
    polys=hexPoly(hexpts)# polygons
    out = pysal.open(outFile+'.shp','w')
    outd = pysal.open(outFile+'.dbf','w')
    outd.header = fieldHead
    outd.field_spec = fieldSpec
    for line in inCOD:
        outd.write(map(float,line.split()))
    outd.close()
    for bbox,poly in polys:
        poly = map(pysal.cg.shapes.Point,poly)
        poly = pysal.cg.shapes.Polygon(poly)
        out.write(poly)
    out.close()
    return 'Shapefile created'

def getBmusPts(bmus,outF,datFile=None):
    """Convert bmus codebook into proper xy coords for hexagon shape
    If datFile given, appends names of MSA's"""
    fo=open(bmus)
    bmus=fo.readlines()
    dims,topo,x,y,neigh = bmus.pop(0).split()
    x=int(x)
    y=int(y)
    hexpts=hexPtsBmus(y,x)
    bmusHex=open(outF,'w')
    bmusHex.write('x,y,q')
    if datFile:
        bmusHex.write(',names')
        dat=open(datFile)
        names=dat.readlines()[2:]
    bmusHex.write('\n')
    for line in range(len(bmus)):
        x,y,q=bmus[line].strip('\n').split()
        nline=[hexpts[(int(x),int(y))][0],hexpts[(int(x),int(y))][1],q]
        nline=','.join(map(str,nline))
        if datFile:
            msa=','+names[line].split()[-1]
            nline+=msa
        nline+='\n'
        bmusHex.write(nline)
    fo.close()
    bmusHex.close()
    return 'Csv created'

def runSom(somPakF,datIn,cols,rows,topo,neigh,rlen1,alpha1,radious1,rlen2,alpha2,radious2,nameO):
    """ 
    Runs all the stages in the som
    ...

    Parameters
    ----------

    somPakF                 : string
                              folder of SOM_PAK
    datIn                   : string
                              full path to the input data
    cols,rows,topo,neigh    : strings
                              all strings as in runSom
    nameO                   : string
                              full path to the output with no file extension
    
    Arguments
    ---------
    qerror                  : float
                              Average quatization error. For each input sample vector
                              the BMU in the map is searched for and the average of
                              the respective quantization errors is returned
        """
    cmd='%srandinit -din %s -cout %s -xdim %s -ydim %s -topol %s -neigh %s'\
            %(somPakF,datIn,nameO+'.cod',cols,rows,topo,neigh)
    os.system(cmd)
    print 'Map initialized'
    cmd='%svsom -din %s -cin %s -cout %s -rlen %s -alpha %s -radius %s'\
            %(somPakF,datIn,nameO+'.cod',nameO+'_1.cod',rlen1,alpha1,radious1)
    os.system(cmd)
    print 'First round run'
    cmd='%svsom -din %s -cin %s -cout %s -rlen %s -alpha %s -radius %s'\
            %(somPakF,datIn,nameO+'_1.cod',nameO+'_2.cod',rlen2,alpha2,radious2)
    os.system(cmd)
    print 'Second round run'
    cmd = '%sqerror -din %s -cin %s'\
            %(somPakF, datIn, nameO+'_2.cod')
    qerror = cmds.getoutput(cmd)
    qerror = float(qerror.split(' is ')[1].split(' ')[0])
    cmd='%sumat -cin %s > %s'%(somPakF,nameO+'_1.cod',nameO+'_umat1.eps')
    os.system(cmd)
    cmd='%sumat -cin %s > %s'%(somPakF,nameO+'_2.cod',nameO+'_umat2.eps')
    os.system(cmd)
    print 'U-matrices written'
    #tr1=getHexShp(nameO+'_1.cod',nameO+'_1_tr')
    tr2=getHexShp(nameO+'_2.cod',nameO+'_2_tr')
    print 'Hexa shapefiles written'
    cmd='%svisual -din %s -cin %s -dout %s'%(somPakF,datIn,nameO+'_1.cod',\
            nameO+'_1.xy')
    os.system(cmd)
    print 'Coords from first round written'
    cmd='%svisual -din %s -cin %s -dout %s'%(somPakF,datIn,nameO+'_2.cod',\
            nameO+'_2.xy')
    os.system(cmd)
    print 'Coords from second round written'
    xy1=getBmusPts(nameO+'_1.xy',nameO+'_1.csv',datIn)
    xy2=getBmusPts(nameO+'_2.xy',nameO+'_2.csv',datIn)
    rel1 = relocateFile(nameO+'_1.csv', nameO+'_1circle.csv', 0.25)
    rel1 = relocateFile(nameO+'_2.csv', nameO+'_2circle.csv', 0.25)

    return qerror

def bestMap(cycles, somPakF, datIn, cols, rows, topo, neigh, rlen1, alpha1, radious1,
        rlen2, alpha2, radious2, nameO, verbose=True):
    """
    Run a SOM procedure several times and retain the best one (minimum qerror)
    ...

    Parameters:
    -----------

    cycles      : int
                  Number of iterations to be run
    runSom pars

    """
    t0 = time.time()
    wd, name = '/'.join(nameO.split('/')[:-1]), nameO.split('/')[-1]
    cmd = 'mkdir %s'%(wd + '/TEMP')
    os.system(cmd)
    qerror = runSom(somPakF,datIn,cols,rows,topo,neigh,rlen1,alpha1,radious1,rlen2,alpha2,radious2, wd + '/TEMP/' + name)
    if verbose:
        print '\n\t%i   qerror of run: %.4f\n'%(cycles, qerror)
    while cycles > 1:
        cmd = 'mkdir %s'%(wd + '/RUNNING')
        os.system(cmd)
        qerrorR = runSom(somPakF,datIn,cols,rows,topo,neigh,rlen1,alpha1,radious1,rlen2,alpha2,radious2, wd + '/RUNNING/' + name)
        if verbose:
            print '\n\t%i   qerror of run: %.4f\n'%(cycles - 1, qerrorR)
            print 'qerror: %.4f qerrorR: %.4f'%(qerror, qerrorR)
        if qerrorR < qerror:
            print 'Updating optimal solution'
            cmd = 'rm -R %s'%(wd + '/TEMP')
            os.system(cmd)
            cmd = 'mv %s %s'%(wd + '/RUNNING', wd + '/TEMP')
            os.system(cmd)
            qerror = qerrorR
        else:
            cmd = 'rm -R %s'%(wd + '/RUNNING')
            os.system(cmd)
        cycles = cycles - 1
    up, folder = '/'.join(wd.split('/')[:-1]), wd.split('/')[-1]
    cmd = 'mv %s %s'%(wd + '/TEMP', up + '/TEMP')
    os.system(cmd)
    cmd = 'rm -R %s'%wd
    os.system(cmd)
    cmd = 'mv %s %s'%(up + '/TEMP', wd)
    os.system(cmd)
    t1 = time.time()
    print '\n\tFinal time: %.4f minutes'%((t1 - t0)/60)
    print '\tSelected qerror: %.4f\n'%qerror
    return 'All set!!!'

def relocate(n,xy,r):
    """Gives back n new coordinates (xys) on a circle of radious r around the point
    xy which is (x,y)
    NOTE: coords need to be floats"""
    xys=[]
    for i in range(n):
        angle=(2*pi/n)*i
        x=xy[0]+r*cos(angle)
        y=xy[1]+r*sin(angle)
        xys.append((x,y))
    print 'Points relocated around point: (%s,%s)'%(str(xy[0]),str(xy[1]))
    return xys

def relocateFile(inFile, oFile, radius):
    """
    Takes xy csv with overlaying points and distributes them across circles
    """
    lines=[]
    fo=open(inFile)
    h=fo.readline()
    for line in fo:
        lines.append(line.strip('\n').split(','))
    fo.close()

    coord2id={}
    for id,line in enumerate(lines):
        xy=tuple(map(float,[line[0],line[1]]))
        if xy in coord2id:
            coord2id[xy].append(id)
        else:
            coord2id[xy]=[id]
    nuLines=copy.copy(lines)
    for point in coord2id:
        if len(coord2id[point])>1:
            circPts=relocate(len(coord2id[point]),point,radius)
            for i,id in enumerate(coord2id[point]):
                nuLines[id][0]=str(circPts[i][0])
                nuLines[id][1]=str(circPts[i][1])
    fo=open(oFile,'w')
    fo.write(h)
    for line in nuLines:
        line=','.join(line)
        line+='\n'
        fo.write(line)
    fo.close()
    return 'Done'

def trNetTricks(SOM_PAKf,data,trNet,oName):
    """Function to get the following out of a trained SOM:
    * Dist. from each neuron to its bmu: minimum distance observation (mdo)
    * Dist. from each neuron to the average observation: distance to average (dta)

    ToDo:
    - Fix .dat file to make it look like a codeBook (i.e. add topo, etc.
      flags)
    """
    cmd='%svisual -din %s -cin %s -dout %s'\
            %(SOM_PAKf,trNet,data,oName+'_mdo.xy')
    os.system(cmd)
    print 'Minimum distance observation created in: ',oName+'_mdo.xy'
    mdoShp=getHexShp(oName+'_mdo.xy',oName+'_mdo')
    print 'ShapeFile written to: ',oName+'_mdo.shp'

    fo=open(data)
    head,n,lines=fo.readline(),fo.readline(),fo.readlines()
    fo.close()
    dat=[]
    for line in lines:
        line=map(float,line.strip('\n').split()[:int(n.strip('\n'))])
        dat.append(line)
    dat=N.array(dat)
    avo=N.mean(dat,axis=0)
    fo=open(oName+'_avo.dat','w')
    fo.write(head)
    fo.write(n)
    line=' '.join(map(str,avo))
    line+='\n'
    fo.write(line)
    fo.close()
    cmd='%svisual -din %s -cin %s -dout %s'\
            %(SOM_PAKf,trNet,oName+'_avo.dat',oName+'_dta.xy')
    os.system(cmd)
    print 'Distance to average observation written to: ',oName+'_dta.xy'
    dta=getHexShp(oName+'_dta.xy',oName+'_dta')
    print 'ShapeFile written to: ',oName+'_dta.shp'
    
    print '\nAll set!!!\n'

