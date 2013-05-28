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

e1,l1,b1 = ReadFile('out1_data_with_msps.txt')
e2,l2,b2 = ReadFile('in1_bubbles_1.5GeV.3GeV.txt')


print (len(e1)-6000)
BGDensity = (len(e1)-6000)/(10.*40.)

nmins  = np.linspace(2,7,11)
count_msps, count_no_msps = [], []


for n in nmins:
    eps = 0.4
    nmin = BGDensity*np.pi*eps**2 + n*np.sqrt(BGDensity*np.pi*eps**2)
    
    mcSims = [[l1,b1],[l2,b2]]
    dbscanResults = MCSTATS.DBSCAN_Compute_Clusters(mcSims, eps=eps, min_samples=nmin,plot =False)
    sigs = MCSTATS.Cluster_Sigs_BG(dbscanResults,BGDensity, BGTemplate = 'BGRateMap.pickle',angularSize = 10.,numProcs = 1)
    

    count_msps.append(len(np.where(sigs[0]>2.0)[0]))
    count_no_msps.append(len(np.where(sigs[1]>2.0)[0]))

plt.errorbar(nmins, count_msps, yerr=np.sqrt(count_msps),label = 'With MSPs')
plt.errorbar(nmins, count_no_msps, yerr=np.sqrt(count_no_msps),label = 'IGBG')
#plt.hist(sigs[0], bins=np.linspace(0,10,21),histtype='step', label='With MSP')
#plt.hist(sigs[1], bins=np.linspace(0,10,21),histtype='step', label='IGBG')



plt.legend()
#plt.scatter(l1, b1, s=1)
plt.show()



    

