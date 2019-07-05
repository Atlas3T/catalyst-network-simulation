import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
import os.path
import time
import multiprocessing as mp
import random
from multiprocessing import Pool
from math import sqrt
import itertools

def getFilePathRoot():
    return os.path.normpath("/home/simuser/local-data/")

def getLatencyDistFilePath(N,p, latname):
    return os.path.normpath(getFilePathRoot() + '/latency_dist_' + str(N) + '_' + str(p) + "_" + str(latname) + '.mat')

def saveLatencyDist(N,p, latencies, latname):
    start = time.time()
    fileName = getLatencyDistFilePath (N,p, latname)
    scipy.io.savemat(fileName, {"latencies" : latencies}, appendmat=True)
    print("saved " + str(fileName) + " in " + str(time.time()-start) + "secs.")

def verifyFilePath(N,p,lat_sum):
    fileName = getLatencyDistFilePath (N, p, lat_sum)
    return os.path.isfile(fileName)

def loadLatenciesDist(N,p,lat_sum):
    fileName = getLatencyDistFilePath (N, p,lat_sum)
    contents = scipy.io.loadmat(fileName, appendmat=True)
    latencies = contents['latencies']
    return latencies

