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
np.set_printoptions(threshold=np.nan)


#N: total number of nodes in pool (validators)
#V: total number of working validators nodes (workers) 
#O: total number of malicious nodes in pool (malicious validators)
#p: total number of malicious nodes selected for validation (malicious workers)
#Vmin: mininim number of validating nodes (minimum hashes collected by a worker for a valid ratio r_i = m/V_i where V_min <= V_i <= V)
#R = O/N

#Probabiliy of p malicious nodes selected for validation
#P(p) = binomial_coefficient(O,p) * binomial_coefficient(N-O,V-p) / binomial_coefficient(N,V)
#SF (survival function = 1 - cumulative Hypergeometric distribution),
#With positive for max(0, O + V - N)< p < min(O,V)# P(p) = pmf(p, N , O, V)

#Range considered for
#p0m = V_min/2 + 1
#p0 = V/2 + 1
#[p0m,V] (more realistic)
#[p0,V] (assume perfeect system)

#Vmin = RV * V


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


def plot_cummulative_over_rangeVmin(rO,N,V,rVmin):
        pH=[]
        pB=[]
        O=N*rO
        print("N, O, V : ",N,", ",O,", ",V,",. varying Vmin:")
    
        for rVi in rVmin:
            pmin = math.floor(rVi/2) + 1
            pH.append(100*hypergeom.sf(pmin, N, O, V))
            print(O," --> ", hypergeom.sf(pmin, N, O, V))
            pB.append(100*binom.sf(pmin,V,rO))
        return (pH,pB)



N = 10000
V = 2000
rR = [0.1,0.2,0.3,0.4,0.45]
Vmin = 500

#Plot for {O}

(p1_O,p2_O) = plot_cummulative_over_rangeO(rR,N,V)
plt.plot(rR,p1_O, label='hypergeometric dist')
plt.plot(rR, p2_O, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Ratio (O/N)')
plt.ylabel('Probability 51% attack')
plt.legend(loc='upper left')
plt.show()

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
plt.ylabel('Probability 51% attack [%]')
plt.hlines(0.00001, Vmin, V, colors='k', linestyles='dashed', label='0.00001% threshold')
plt.legend(loc='lower left')
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),))
y_text = 1000000*min(p1_V)
plt.text(Vmin,y_text, textstr, fontsize=10)
plt.show()



Vmin=1600
rVmin = range(Vmin, V+1, 50)
O = math.floor(rR1*N)
p1_Vmin = ""
textstr = '\n'.join((
    r'N = %.d' % (N, ),
    r'O = %.d' % (O, ),
    r'V = %.d' % (V, ),))
#y_text = 1000000*rR1
#Plot for {Vmin}
(p1_Vm,p2_Vm) = plot_cummulative_over_rangeVmin(rR1,N,V,rVmin)
plt.plot(rVmin, p1_Vm, label='hypergeometric dist')
plt.plot(rVmin, p2_Vm, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Vmin')
plt.ylabel('Probability 51% attack [%]')
plt.hlines(0.00001, Vmin, V, colors='k', linestyles='dashed', label='0.00001% threshold')
plt.legend(loc='lower left')
plt.text(Vmin,y_text, textstr, fontsize=10)
plt.show()




#Probability of attack < 10-6 (1 chance of attacking in a million)
#For a given O = 40% (or 3 O = 3 curves)



#Find the ratio V/N from which the probability < 10-6


def plot_ratio_VoverN(rO,rN,thre):
        pH=[]
        for rNi in rN:
            O=rNi*rO
            print("N, O: ",rNi,", ",O,". Varying V to find proba ~ 10-6")
            Vmin = math.floor(0.001*rNi)
            Vmax = math.floor(0.2*rNi)
            rangeV = range(Vmin,Vmax,100)
            proba_thre = 1
            rVi = Vmin
            Vbin = 10
            V_thre = 0
            while proba_thre > thre:
                p = math.floor(rVi/2) + 1
                proba_thre = hypergeom.sf(p, rNi, O, rVi)
                V_thre = rVi
                #print(rVi,", prob --> ",proba_thre)
                rVi = rVi + Vbin
            #print("--> ",V_thre/N) 
            pH.append(V_thre/N)
        return (pH)
    
proba_thre = 0.000000001
rangeN = range(5000,100000,1000)
rO=0.2
p1VoN_1 = plot_ratio_VoverN(rO,rangeN,proba_thre)
rO=0.3
p1VoN_2 = plot_ratio_VoverN(rO,rangeN,proba_thre)
rO=0.4
p1VoN_3 = plot_ratio_VoverN(rO,rangeN,proba_thre)
plt.plot(rangeN,p1VoN_1, label='20% malicious')
plt.plot(rangeN,p1VoN_2, label='30% malicious')
plt.plot(rangeN,p1VoN_3, label='40% malicious')
plt.xlabel('N')
plt.ylabel('V/N (prob < 10-9)')
plt.legend(loc='upper left')
plt.show()


#bla bla ignore following

rangeV = range(Vmin, V, 50)

#plot_cummulative_over_V(rangeV,N,R)

#Vm = np.arange(100,5000, 50)

#(p1,p2) = plot_cummulative_over_V(Vm,10000,0.3)
(p1,p2) = plot_cummulative_over_rangeO(rR,N,V)
plt.plot(rR,p1, label='hypergeometric dist')
plt.plot(rR, p2, label = 'binomial approx.')
plt.yscale('log')
plt.xlabel('Ratio (O/N)')
plt.legend(loc='upper left')
