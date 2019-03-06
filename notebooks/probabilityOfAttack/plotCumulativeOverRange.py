from scipy.stats import hypergeom
from scipy.stats import binom
from decimal import *
import numpy as np
import os
import math
from cycler import cycler
#%matplotlib inline  
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
#np.set_printoptions(threshold=np.nan)

#N: total number of nodes in pool (validators)
#V: total number of working validators nodes (workers) 
#O: total number of malicious nodes in pool (malicious validators)
#p: total number of malicious nodes selected for validation (malicious workers)
#Vmin: mininim number of validating nodes (minimum hashes collected by a worker for a valid ratio r_i = m/V_i where V_min <= V_i <= V)

def plot_cummulative_over_rangeO(rR,N,V):
        
        pH=[]
        pB=[]
        p = math.floor(V/2) + 1
        print("N, V: ",N,", ",V,". Varying O:")
        for rRi in rR:
            O=N*rRi
            pH.append(hypergeom.sf(p, N, O, V))
            print(O," --> ", hypergeom.sf(p, N, O, V))
            pB.append(binom.sf(p,V,rRi))
        return (pH,pB)


N = 10000
V = 2000
rR = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
Vmin = 500
#Plot for {O}
(p1_O,p2_O) = plot_cummulative_over_rangeO(rR,N,V)
plt.plot(rR,p1_O, label='hypergeometric dist')
plt.plot(rR, p2_O, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Ratio (O/N)')
plt.ylabel('Probability 51% attack')
plt.title('Probability of attack for ratios of total malicious nodes')
plt.legend(loc='upper left')
plt.savefig('Graphs/plot_cummulative_over_range.png')