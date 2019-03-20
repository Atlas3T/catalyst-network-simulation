from Graph_gen import plot_ratio_VoverN
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


#This plot describes O at 20%, 30%, 40% and 45% of vairying N values and the minimum V/N value needed to obtain 10^-9 security



proba_thre = 10**-9
rangeN = range(5000,51000,1000) #Will stay the same as this determines the range of N
top = rangeN[-1] 
bottom = rangeN[0] 
Ovalues = [0.3,0.4,0.45]
#create string for VoN labels 
strRangeO = '-'.join(str(e) for e in Ovalues)
print("Generating graphs....")
curves = []
for rO in Ovalues:
    curve = plot_ratio_VoverN(rO,rangeN,proba_thre)
    curves.append(curve)
for ind_curve in range(0,len(Ovalues)):
    fO = math.floor(100*Ovalues[ind_curve])
    plt.plot(rangeN,curves[ind_curve],label='{}%'.format(fO))
top2 = top/10
plt.grid()
plt.ylim(0,0.5) #may have to be increased for higher thresholds
plt.yticks(np.arange(0, 0.55, step=0.05)) #may have to be increased for higher thresholds
if bottom < 3000:
    plt.xticks(np.arange(3000, top+top2, step=top2))
    plt.xlim(3000,top)
    print('rangeN to low to give accuracte results, readjusting range')
else:
    plt.xticks(np.arange(bottom-top2, top+top2, step=top2))
    plt.xlim(bottom,top)
plt.xlabel('N (total worker pool size)')
plt.ylabel('Ratio of V/N for prob < {}'.format(proba_thre))
plt.legend(title='Percentage O/N',loc='upper right')
plt.savefig('Graphs/graph_V_over_N_at_prob_{}vs_N_for_range_{}_to_{}_O_at_{}.png'.format(proba_thre,bottom,top,strRangeO))

