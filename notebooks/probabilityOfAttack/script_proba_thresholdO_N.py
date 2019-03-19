from scipy.stats import hypergeom
from scipy.stats import binom
from decimal import *
import numpy as np
import os
import math
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter

def plot_thresholdO_over_N(rN, rVoN, threshold):
    #rVoN: a ratio
    #rN: range of N values
    curveOoN=[]
    for irN in rN:
        V = math.floor(irN * rVoN)
        binO = 0.001
        itO = 0.01
        max_fracO = 0
        proba = 0
        #print("V ",V, " and N ", irN) 
        while proba < threshold:
            p = math.floor(V/2) + 1
            O = math.floor(itO*irN)
            proba = hypergeom.sf(p,irN,O, V)
            max_fracO = itO
            itO = itO + binO
            #print("test ",O," --> ",proba) 
        #print(" ---> max_fracO ",  max_fracO)     
        curveOoN.append(max_fracO)
    return curveOoN
        #print(curveOoN)


#x-axis: N
#rangeN = [1000, 2000, 10000]
#rangeN = [2000, 5000]
rangeN = range(1000,20500,500)
top = rangeN[-1] 
bottom = rangeN[0] 
#y-axis: fraction O/N
#curves: different ratio V/N
rangeVoN = [0.01,0.05,0.1,0.2,0.3]

strRangeVoN = '-'.join(str(e) for e in rangeVoN)
   

#variables: probability threshold
prob_thre = 10**-9
curves = []

ind_curve = 0
curves = []
for irVoN in rangeVoN:
    curve = plot_thresholdO_over_N(rangeN, irVoN , prob_thre)
    #print(curve)
    curves.append(curve)
print(len(rangeVoN))
for ind_curve in range(0,len(rangeVoN)):    
    #print(ind_curve," --> ", curves[ind_curve])
    fVoN = math.floor(100*rangeVoN[ind_curve])
    bla = print("bla for ", fVoN, "N")
    plt.plot(rangeN,curves[ind_curve],label='{} percent ratio V/N'.format(fVoN))
print(rangeN)
plt.grid()    
plt.xlabel('N (total number of nodes)')
plt.ylabel('Max O/N for prob < {}'.format(prob_thre))
plt.legend(loc='lower right')
plt.savefig('Graphs/O-over-N-{}-{}-for-V-over-N-{}.png'.format(bottom,top,strRangeVoN))