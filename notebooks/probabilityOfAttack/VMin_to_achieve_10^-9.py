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

#This plot describes O at 20%, 30%, 40% and 45% of vairying N values and the minimum V/N value needed to obtain 10^-6 security


def plot_ratio_VMinOverN(rO,rN,thre):
        pH=[]
        for rNi in rN: #Will stay the same as we want x axis to be over N
            O=rNi*rO #Will stay the same as we want to show vairying mallicious nodes
            #print("N, O: ",rNi,", ",O,". Varying V to find proba ~ $10^-9$") #Stays the same
            V = rNi*0.2 #Set the V to N ratio
            Vmin = math.floor(0.001*V)
            proba_thre = 1
            rVi = Vmin

            Vbin = 5
            VMin_thre = 0
            while proba_thre > thre:
                p = math.floor(rVi/2) 
                proba_thre = hypergeom.sf(p, rNi, O, rVi)
                VMin_thre = rVi
                #print(rVi,", prob --> ",proba_thre)
                rVi = rVi + Vbin
            #print("--> ",V_thre/N)
            pH.append(VMin_thre/V) #Needs to be VMin_thre / V
        return (pH)


proba_thre = 0.000000001
rangeN = range(15000,100000,1000) #Will stay the same as this determines the range of N
print("Generating graphs....")
#rO=0.2
#p1VMinoN_1 = plot_ratio_VMinOverN(rO,rangeN,proba_thre)
rO=0.3
p1VMinoN_2 = plot_ratio_VMinOverN(rO,rangeN,proba_thre) 
rO=0.4
p1VMinoN_3 = plot_ratio_VMinOverN(rO,rangeN,proba_thre)
rO=0.45
p1VMinoN_4 = plot_ratio_VMinOverN(rO,rangeN,proba_thre) 
#plt.plot(rangeN,p1VMinoN_1, label='20% malicious nodes')
plt.plot(rangeN,p1VMinoN_2, label='30% malicious nodes')
plt.plot(rangeN,p1VMinoN_3, label='40% malicious nodes')
plt.plot(rangeN,p1VMinoN_4, label='45% malicious nodes')
plt.xlabel('N (total number of nodes)')
plt.ylabel('Ratio of VMin/Min for prob < $10^{-9}$')
plt.legend(loc='upper right')
plt.savefig('Graphs/graph_VMin_over_V_at_prob_10^-9vs_N_for_range_15000_to_100000_O_at_30_40_45.png')