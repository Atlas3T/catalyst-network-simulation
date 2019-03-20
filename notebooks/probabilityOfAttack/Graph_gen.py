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

def plot_ratio_VoverN(rO,rN,thre):
        pH=[]
        for Ni in rN: #For each rangeN in range 5k - 100k
            O=Ni*rO #O = Each range x the ratio of bad nodes specified 
            #print("N, O: ",Ni,", ",O,". Varying V to find proba ~ 10-9")
            Vmin = math.floor(0.001*Ni) #Minumum value of V is 0.001 of the value of the range interval 
            #Vmin = math.max(V_min as defined in the parameters of the fonction 2000, math.floor(0.001*Ni))
            proba_thre = 1 
            rVi = Vmin #rVi is set to 0.001 of the value of the range interval 
            Vbin = 5 #bin size of 10 
            V_thre = 0 
            while proba_thre > thre: #while value set on l32 > value set on l52 ...
                p = math.floor(rVi/2) + 1 #math.floor rounds to the nearest value 
                proba_thre = hypergeom.sf(p, Ni, O, rVi)
                V_thre = rVi
                #print(rVi,", prob --> ",proba_thre)
                rVi = rVi + Vbin
            #print("--> ",V_thre/N) 
            pH.append(V_thre/Ni)
        return (pH)

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


def plot_thresholdO_over_N(rN, rVoN, threshold):
    #rVoN: a ratio
    #rN: range of N values
    curveOoN=[]
    for irN in rN:
        V = math.floor(irN * rVoN)
        binO = 0.001
        itO = 0.001
        max_fracO = 0
        proba = 0
        while proba < threshold:
            p = math.floor(V/2) + 1
            O = math.floor(itO*irN)
            proba = hypergeom.sf(p,irN,O, V)
            max_fracO = itO
            itO = itO + binO    
        curveOoN.append(max_fracO)
    return curveOoN

def plot_cummulative_over_rangeO(rR,N,V):
        
        pH=[]
        pB=[]
        p = math.floor(V/2) + 1
        #print("N, V: ",N,", ",V,". Varying O:")
        for rRi in rR:
            O=N*rRi
            pH.append(hypergeom.sf(p, N, O, V))
            #print(O," --> ", hypergeom.sf(p, N, O, V))
            pB.append(binom.sf(p,V,rRi))
        return (pH,pB)


def plot_multiple_cummulative_over_rangeO(rR,N,V):
        
        pH=[]
        pB=[]
        p = math.floor(V/2) + 1
        #print("N, V: ",N,", ",V,". Varying O:")
        for rRi in rR:
            O=N*rRi
            pH.append(hypergeom.sf(p, N, O, V))
            #print(O," --> ", hypergeom.sf(p, N, O, V))
        return (pH)

def plot_cummulative_over_rangeV(rO,N,rV):
        pH=[]
        pB=[]
        O=N*rO
        #print("N, O: ",N,", ",O,". Varying V:")
        for rVi in rV:
            p = math.floor(rVi/2) + 1
            pH.append(100*hypergeom.sf(p, N, O, rVi))
            #print(O," --> ", hypergeom.sf(p, N, O, rVi))
            pB.append(100*binom.sf(p,rVi,rO))
        return (pH,pB)        

def plot_cummulative_over_rangeVmin(rO,N,rVmin):
        pH=[]
        pB=[]
        O=N*rO
    
        for rVi in rVmin:
            pmin = math.floor(rVi/2) + 1
            pH.append(hypergeom.sf(pmin, N, O, rVi))
            #print(O," --> ", hypergeom.sf(pmin, N, O, rVi))
            pB.append(binom.sf(pmin,rVi,rO))
        return (pH,pB)        