import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
from functools import partial
import os.path
import profile
import time

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/peer_dist/test/")


def getPeerDistEvenFaster(N, p, i):
    start = time.time()
    peers =  numpy.full((N, p), -1, dtype = int)
    
    # array to randomly shuffle each iteration to give us potential peers in different order
    nodes = numpy.arange(N)
    rand = numpy.random.randint

    pn = peersNeededfunc
    fvp =findPeersForNode

    # nasty code for the sake of speed. fvp returns false when valid peer row can't be made so that we fail
    # early. Otherwise it updates peers.
    if any(fvp(peers, nodes, peersNeededfunc,rand, N, p, i) for i in range(0,N)): 
            getPeerDistEvenFaster(N,p,i)
        break;
    if isValid(peers,N,p):
        print("found one in " + str(time_now-start) + "secs.")
        savePeerDist(N,p,peerDist,i)
    else getPeerDistEvenFaster(N,p,i)

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
    step = 1 if N <= 1000 else N/100    #we are going to risk not checking every set of peers to save time for larger numbers of nodes.
    for i in range(0,step,N):
        if numpy.count_nonzero(peers==i)!=p: #each peer should appear exactly p times.
            return False
    return True

def generatePeerDistMultiple(N,p,n):
    start = time.time()
    item_start = start
    i = 0
    for peerDist in getPeerDistOrDieTrying(N,p):
        time_now = time.time()
        i+=1
        print("found one in " + str(time_now-item_start))
        savePeerDist(N,p,peerDist,i)
        if(i==n):
            av_time = (time_now - start)/n
            print("time taken: " +  str(av_time))
            break
        item_start = time.time()

def getPeerDistForever(N,p):
    while True:
        yield from getPeerDistEvenFaster(N,p)

def getPeerDistOrDieTrying(N,p):
    for item in getPeerDistForever(N,p):
        if isValid(item,N,p):
            yield item



def getPeerDistFilePath(N,p,i):
    return os.path.normpath(getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(i))


def savePeerDist(N,p,peers,i):
    start = time.time()
    fileName = getPeerDistFilePath(N,p,i)
    scipy.io.savemat(fileName, {"peers" : peers}, appendmat=True)
    print("saved " + str(fileName) + "in" + str(time.time()-start) + "secs.")

def loadPeerDist(N,p,i):
        fileName = getPeerDistFilePath(N, p, i)
        contents = scipy.io.loadmat(fileName, appendmat=True)
        peers = contents['peers']
        return peers









