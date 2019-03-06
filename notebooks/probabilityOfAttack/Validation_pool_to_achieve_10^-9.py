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


#This plot describes O at 20%, 30%, 40% and 45% of vairying N values and the minimum V/N value needed to obtain 10^-9 security

def plot_ratio_VoverN(rO,rN,thre):
        pH=[]
        for rNi in rN: #For each rangeN in range 5k - 100k
            O=rNi*rO #O = Each range x the ratio of bad nodes specified 
            print("N, O: ",rNi,", ",O,". Varying V to find proba ~ 10-9")
            Vmin = math.floor(0.001*rNi) #Minumum value of V is 0.001 of the value of the range interval 
            
            proba_thre = 1 
            rVi = Vmin #rVi is set to 0.001 of the value of the range interval 
            Vbin = 10 #bin size of 10 
            V_thre = 0 
            while proba_thre > thre: #while value set on l32 > value set on l52 ...
                p = math.floor(rVi/2) + 1 #math.floor rounds to the nearest value
                proba_thre = hypergeom.sf(p, rNi, O, rVi)
                V_thre = rVi
                #print(rVi,", prob --> ",proba_thre)
                rVi = rVi + Vbin
            #print("--> ",V_thre/N) 
            pH.append(V_thre/N)
        return (pH)


N = 10000
V = 2000



proba_thre = 0.000000001
rangeN = range(5000,100000,1000)
rO=0.2
p1VoN_1 = plot_ratio_VoverN(rO,rangeN,proba_thre)
rO=0.3
p1VoN_2 = plot_ratio_VoverN(rO,rangeN,proba_thre)
rO=0.4
p1VoN_3 = plot_ratio_VoverN(rO,rangeN,proba_thre)
rO=0.45
p1VoN_4 = plot_ratio_VoverN(rO,rangeN,proba_thre)
plt.plot(rangeN,p1VoN_1, label='20% malicious nodes')
plt.plot(rangeN,p1VoN_2, label='30% malicious nodes')
plt.plot(rangeN,p1VoN_3, label='40% malicious nodes')
plt.plot(rangeN,p1VoN_4, label='45% malicious nodes')
plt.title('V/N threshold needed for a probability of attack < $10^{-9}$')
plt.xlabel('N (total number of nodes)')
plt.ylabel('Ratio of V/N for prob < $10^{-9}$')
plt.legend(loc='center right')
plt.savefig('Graphs/V_ratio_for_10^-9.png')