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

#N: total number of nodes in pool (validators)
#V: total number of working validators nodes (workers) 
#O: total number of malicious nodes in pool (malicious validators)
#p: total number of malicious nodes selected for validation (malicious workers)
#Vmin: mininim number of validating nodes (minimum hashes collected by a worker for a valid ratio r_i = m/V_i where V_min <= V_i <= V)

#This generates a graph demostrating the minimum number (Vmin) of nodes that report the correct delta needed to generate acceptable security levels. 
#

def plot_cummulative_over_rangeVmin(rO,N,V,rVmin):
        pH=[]
        pB=[]
        O=N*rO
        #print("N, O, V : ",N,", ",O,", ",V,",. varying Vmin:")
    
        for rVi in rVmin:
            pmin = math.floor(rVi/2) + 1
            pH.append(100*hypergeom.sf(pmin, N, O, V))
            print(O," --> ", hypergeom.sf(pmin, N, O, V))
            pB.append(100*binom.sf(pmin,V,rO))
        return (pH,pB)

N = 10000
V = 2000
rR = [0.1,0.2,0.3,0.4,0.45]
rR1 = 0.4

Vmin=1600
rVmin = range(Vmin, V+1, 50)
O = math.floor(rR1*N)
p1_Vmin = ""
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),
    r'V = %.d' % (V, ),))
y_text = 1000000*rR1
#Plot for {Vmin}
(p1_Vm,p2_Vm) = plot_cummulative_over_rangeVmin(rR1,N,V,rVmin)
plt.plot(rVmin, p1_Vm, label='hypergeometric dist')
plt.plot(rVmin, p2_Vm, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Vmin')
plt.ylabel('Probability 51% attack [%]')
plt.hlines(0.000000001, Vmin, V, colors='k', linestyles='-.', label='0.000000001% threshold')
plt.hlines(0.000001, Vmin, V, colors='k', linestyles='dashed', label='0.000001% threshold')
plt.legend(loc='lower left')
plt.title('Probability of attack vs VMin against 40% malicious nodes')
plt.text(Vmin,y_text, textstr, fontsize=10, position=(1600, 6.737358984570953e-15),  bbox=dict(facecolor='none', edgecolor='red'))
plt.savefig('Graphs/VMin.png')