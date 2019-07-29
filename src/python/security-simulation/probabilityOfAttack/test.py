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
import matplotlib as mpl

mpl.rcParams['hatch.linewidth'] = 0.1
mpl.rcParams['hatch.linewidth'] = 0.1
r = 0.7
V = 100
delta_r = 4.22*math.sqrt(r*(1-r)/V)
data       = [r,1-r]
y,binEdges = np.histogram([0.7,0.3],bins=[1,2])
print(y)
print(binEdges)
bincenters = binEdges+0.5*(binEdges[1:]+binEdges[:-1])
print(bincenters)
menStd     = [delta_r,delta_r]
datam     = [r-delta_r,1-r-delta_r]
datap     = [r-delta_r,1-r+delta_r]
width      = 1
plt.bar(bincenters, data, width=width, color='w',edgecolor='black', yerr=menStd)
plt.fill_between(bincenters, datam, datap, set_transform.pass_through=True)
plt.show()
