import numpy as np
from matplotlib import pyplot as plt
import MC2, cPickle as pickle
import multiprocessing as mp
import MCSTATS, csv


def ReadFile(file):
    reader = csv.reader(open(file, 'rb'),delimiter = ' ' )
    e,l,b  = [],[],[]
    for line in reader:
        e.append(float(line[0]))
        b.append(float(line[2]))
        ltmp = float(line[1])
        #l.append(ltmp)
        
        if ltmp > 180: l.append(ltmp-360)
        else: l.append(ltmp)
    return (e,l,b)

#e1,l1,b1 = ReadFile('out1_data_with_msps.txt')
#e2,l2,b2 = ReadFile('in1_bubbles_1.5GeV.3GeV.txt')
#BGDensity = (len(e1)-6000)/(10.*40.)

e1,l1,b1 = ReadFile('out2_data_with_msps_front.txt')
e2,l2,b2 = ReadFile('in2_bubbles_1.5GeV.3GeV.front.txt')
BGDensity = (len(e1)-3000)/(10.*40.)


nmins  = np.linspace(2,7,21)
count_msps, count_no_msps = [], []

#===============================================================================
# Scan nmin
#===============================================================================
#for n in nmins:
#    eps = 0.4
#    nmin = BGDensity*np.pi*eps**2 + n*np.sqrt(BGDensity*np.pi*eps**2)
#    
#    mcSims = [[l1,b1],[l2,b2]]
#    dbscanResults = MCSTATS.DBSCAN_Compute_Clusters(mcSims, eps=eps, min_samples=nmin,numProcs=2, plot =False)
#    sigs = MCSTATS.Cluster_Sigs_BG(dbscanResults,BGDensity, BGTemplate = 'BGRateMap.pickle',angularSize = 10.,numProcs = 1)
#    
#    s1, s2 = np.array(sigs[0]), np.array(sigs[1])
#    
#    print len(np.where(s1>1.0)[0]),len(np.where(s2>1.0)[0])
#    count_msps.append(len(np.where(s1>1.0)[0]))
#    count_no_msps.append(len(np.where(s2>1.0)[0]))
#
#plt.errorbar(nmins, count_msps, yerr=np.sqrt(count_msps),label = 'With MSPs',marker='o')
#plt.errorbar(nmins, count_no_msps, yerr=np.sqrt(count_no_msps),label = 'IGBG',marker='o')
#plt.show()


#===============================================================================
# 
#===============================================================================
eps = 0.6
#n = 4 # 6000
n = 3.0 # 6000

nmin = BGDensity*np.pi*eps**2 + n*np.sqrt(BGDensity*np.pi*eps**2)

mcSims = [[l1,b1],[l2,b2]]
dbscanResults = MCSTATS.DBSCAN_Compute_Clusters(mcSims, eps=eps, min_samples=nmin,numProcs=2, plot =False)
sigs = MCSTATS.Cluster_Sigs_BG(dbscanResults,BGDensity, BGTemplate = 'BGRateMap.pickle',angularSize = 10.,numProcs = 2)

s1, s2 = np.array(sigs[0]), np.array(sigs[1])

values1, bins = np.histogram(s1, bins=np.linspace(0,10,21))
values2, bins = np.histogram(s2, bins=np.linspace(0,10,21))


plt.errorbar(bins[:-1], values1, yerr=np.sqrt(values1),fmt='o',c='b',label = 'MSPs')
plt.errorbar(bins[:-1], values2, yerr=np.sqrt(values2),fmt='o',c='r',label = 'IGBG')
plt.xlabel('s')
plt.ylabel('Count')

plt.legend()
#plt.scatter(l1, b1, s=1)
plt.show()



    

