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
        return (pH)


N = 10000
V = 2000
rR = [0.3,0.35,0.4,0.45,0.5]
#Plot for {O}
p1_O = plot_cummulative_over_rangeO(rR,N,V)
N = 2000
V = 400
p1_1 = plot_cummulative_over_rangeO(rR,N,V)
N = 5000
V = 1000
p1_2 = plot_cummulative_over_rangeO(rR,N,V)
N = 20000
V = 4000
p1_3 = plot_cummulative_over_rangeO(rR,N,V)

plt.plot(rR,p1_1, label='hypergeometric dist. for 2000 nodes')

plt.plot(rR,p1_2, label='hypergeometric dist. for 5000 nodes')

plt.plot(rR,p1_O, label='hypergeometric dist. for 10000 nodes')

plt.plot(rR,p1_3, label='hypergeometric dist. for 20000 nodes')

plt.yscale('log')
plt.xlabel('Fraction of malicious nodes (O) in validation pool set N')
plt.ylabel('Probability 51% attack')
plt.hlines(0.000001, 0.3, 0.5, colors='k', linestyles='dashed', label='0.00001% threshold')
plt.hlines(0.000000001, 0.3, 0.5, colors='k', linestyles='-.', label='0.000000001% threshold')
plt.legend(loc='lower right',prop={'size': 9})
plt.savefig('Graphs/O_over_Several_N.png')