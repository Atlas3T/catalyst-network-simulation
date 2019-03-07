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

def plot_cummulative_over_rangeV(rO,N,rV):
        pH=[]
        pB=[]
        O=N*rO
        print("N, O: ",N,", ",O,". Varying V:")
        for rVi in rV:
            p = math.floor(rVi/2) + 1
            pH.append(100*hypergeom.sf(p, N, O, rVi))
            print(O," --> ", hypergeom.sf(p, N, O, rVi))
            pB.append(100*binom.sf(p,rVi,rO))
        return (pH,pB)


N = 10000
V = 2000
rR1 = 0.4
O = math.floor(rR1*N)
Vmin=500
rV = range(Vmin,V+1,50)
#Plot for {V}
(p1_V,p2_V) = plot_cummulative_over_rangeV(rR1,N,rV)
plt.plot(rV,p1_V, label='hypergeometric dist')
plt.plot(rV, p2_V, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('V')
plt.ylabel('Probability 51% attack')
plt.hlines(0.000001, Vmin, V, colors='k', linestyles='dashed', label='0.00001% threshold')
plt.hlines(0.000000001, Vmin, V, colors='k', linestyles='-.', label='0.000000001% threshold')
plt.legend(loc='lower left')
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),))
y_text = 1000000*min(p1_V)
plt.text(Vmin,y_text, textstr, fontsize=10,bbox=dict(facecolor='none', edgecolor='black'))
plt.savefig('Graphs/graph_prob_vs_V_N10000_O_4000.png')