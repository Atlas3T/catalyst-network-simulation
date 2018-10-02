import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
from functools import partial
import os.path
import profile
import time
import multiprocessing as mp
from multiprocessing import Queue as PQueue
import random
from multiprocessing import Pool
from SharedCounter import SharedCounter
from math import sqrt
import itertools

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/peer_dists/test/")


def getPeerDistEvenFaster(params):
    N = params[0]
    p = params[1]
    i = params[2]
    lock = params[3]
    counter = params[4]
    needed = params[5]

    start = time.time()

    peers =  numpy.full((N, p), -1, dtype = int)
    
    # array to randomly shuffle each iteration to give us potential peers in different order
    nodes = numpy.arange(N)
    rand = numpy.random.randint

    pn = peersNeededfunc
    fvp =findPeersForNode

    # nasty code for the sake of speed. fvp returns false when valid peer row can't be made so that we fail
    # early. Otherwise it updates peers.
    success = False
    if any(fvp(peers, nodes, peersNeededfunc,rand, N, p, i) for i in range(0,N)): 
        return False
    if isValid(peers,N,p):
        doSave = False
        copyOfCounter = 0
        with lock:
            counter.value+=1
            if counter.value<=needed:
                doSave = True
                copyOfCounter = counter.value
        if doSave:
            savePeerDist(N,p,peers,copyOfCounter)
            success = True
    return success

def peersNeededfunc(peers,p,n):
        return p - numpy.count_nonzero(peers[n,:] >= 0)

def findPeersForNode(peers, nodes, peersNeededfunc,randfunc, N, p, i):

    cdef int maxIndices = N-1   #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
    cdef int peersNeeded =  peersNeededfunc(peers,p,i)
    cdef int randPeerIndex
    cdef int potPeer
    
    while(peersNeeded > 0 and maxIndices > 0):

        randPeerIndex = randfunc(0,maxIndices)

        potPeer = nodes[randPeerIndex]

        nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
        maxIndices -= 1

        if potPeer != i and not any(peers[potPeer,:]==i):

            peersNeededByPeer = peersNeededfunc(peers,p,potPeer)
            
            if peersNeededByPeer > 0:
                peers[potPeer,p - peersNeededByPeer] = i
                peers[i, p - peersNeeded] = potPeer
                peersNeeded-=1
    if peersNeeded > 0:
        return True
    else:
        return False

def isValid(peers,N,p):
    if peers == []:
        return False
    step = 1 if N <= 1000 else int(N/100)    #we are going to risk not checking every set of peers to save time for larger numbers of nodes.
    for i in range(0,step,N):
        #each peer should appear exactly p times.
        if numpy.count_nonzero(peers==i)!=p: 
            return False
    return True


def getPeerDistFilePath(N,p,i):
    return os.path.normpath(getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(i))


def savePeerDist(N,p,peers,i):
    start = time.time()
    fileName = getPeerDistFilePath(N,p,i)
    scipy.io.savemat(fileName, {"peers" : peers}, appendmat=True)
    print("saved " + str(fileName) + "in " + str(time.time()-start) + "secs.")

def loadPeerDist(N,p,i):
        fileName = getPeerDistFilePath(N, p, i)
        contents = scipy.io.loadmat(fileName, appendmat=True)
        peers = contents['peers']
        return peers

class run_until_done():
    L = 5   # limit for performance timing 
    N  = 5
    m = mp.Manager()
    counter = m.Value('i',0)
    lock = m.Lock()
    i=0
    pool = Pool()
    before = time.time()
    success_count = 0
    for result in pool.imap_unordered(getPeerDistEvenFaster, itertools.repeat([10000,10,55, lock , counter, N]), 10):
        i+=1
        with lock:
            if counter.value >= N:
                pool.close()
        if result:
            success_count+=1
            if success_count>=N:
                pool.terminate()
                break;
    pool.join()
    print("Computed %d valid distributions in %.1fms. Saved %d, took %d tries." % (counter.value, (time.time()-before)*1000.0,success_count, i))









