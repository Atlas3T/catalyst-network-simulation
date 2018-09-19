import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
from functools import partial
import os.path
import profile
import time

def getPeerDistEvenFaster(N, p):
    peers =  numpy.full((N, p), -1, dtype = int)
    nodes = numpy.arange(N)  # array to randomly shuffle each iteration to give us potential peers in different order
    rand = numpy.random.randint
    
    #pn = partial(peersNeededfunc,peers,p)
    #fvp =partial(findPeersForNode,peers,nodes,pn,rand,N,p)

    pn = peersNeededfunc
    fvp =findPeersForNode
    if any(fvp(peers, nodes, peersNeededfunc,rand, N, p, i) for i in range(0,N)):
        return []
    yield peers

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
    b = peers.flatten()
    for i in range(0,N):
        if numpy.count_nonzero(b==i)!=p:
            return False
    return True

def generatePeerDist(N,p,n):
    start = time.time()
    item_start = start
    i = 0
    for peerDist in getPeerDistOrDieTrying(N,p):
        time_now = time.time()
        i+=1
        print("found one in " + str(time_now-item_start))
        savePeerDist(N,p,peerDist,i+4)
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


def sendToPeers(peers,messageDist,time):
    p = peers[messageDist == time,:]
    messageDist[p[:]]=numpy.where(messageDist[p[:]]==-1,time+1,messageDist[p[:]])
    return messageDist

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/")


def getPeerDistFilePath(N,p,s):
    return os.path.normpath(getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(s))

def getProbDistFilePath(N,p, x, i):
    return getFilePathRoot() + '/prob_dist_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i)

def savePeerDist(N,p,peers,i):

        fileName = getPeerDistFilePath(N,p,i)
        scipy.io.savemat(fileName, {"peers" : peers}, appendmat=True)
        print("saved " + str(fileName) + "at" + str(time.time()))

def loadPeerDist(N,p,n):
        fileName = getPeerDistFilePath(N, p, n)
        contents = scipy.io.loadmat(fileName, appendmat=True)
        peers = contents['peers']
        return peers


def hasMessageSpreadToAllNodes(messageDist):
    return not numpy.any(messageDist==-1)

def disperseMessage(peers,s):
    N = len(peers[:,0])
    messageDist = numpy.full(N,-1)
    time = 0
    messageDist[s] = time
    while (hasMessageSpreadToAllNodes(messageDist)==False):
        messageDist=sendToPeers(peers,messageDist,time)
        time += 1
    return messageDist

def saveDisperseMessageDist(N,p,x,iterations_startNode):
    probDist = dict()
    for ii in range(0,x):
        peers = loadPeerDist(N,p,ii)
        nodes = numpy.arange(N)
        maxIndices = N-1

        for i in range(0,iterations_startNode):
            randStartNodeIndex = numpy.random.randint(0, N-1)
            randNode = nodes[randStartNodeIndex]
            nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
            messageDist = disperseMessage(peers,randNode)
            unique_elements, counts_elements = numpy.unique(messageDist, return_counts=True)
            for j in range(0,len(unique_elements)):
                numOfHops = unique_elements[j]
                if numOfHops in probDist:
                    probDist[numOfHops] += counts_elements[j]
                else:
                    probDist[numOfHops] = counts_elements[j]

    for k in probDist.keys():
        probDist[k]/=(N*iterations_startNode*x)
    X = len(probDist.keys())
    probs: ndarray = numpy.zeros((2,X))
    jj = 0
    for k,v in probDist.items():
        probs[0,jj]=k
        probs[1,jj]=v
        jj+=1
    print(probs)
    fileName = getProbDistFilePath(N, p, x, iterations_startNode)
    scipy.io.savemat(fileName, {"probDist": probs}, appendmat=True)

def loadDisperseMessageDist(N,p,x,iterations_startNode):

    fileName = getProbDistFilePath(N, p, x, iterations_startNode)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    probDist = contents['probDist']
    return probDist








