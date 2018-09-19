import pyximport; pyxinstall()
import numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
import os.path
import profile
import time
numpy.set_printoptions(threshold=numpy.inf)

def getfileSubsetSize():
    return 1

def getPeerDist(N, p):

    peers = numpy.zeros((N, N),dtype = bool)
    nodes = numpy.arange(N)  # array to randomly shuffle each iteration to give us potential peers in different order
    for i in range(0,N):

        peersNeeded = p - sum(peers[i,:])
        maxIndices = N-1     #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
        while(peersNeeded > 0 and maxIndices > 0):

            #selects option for peer and ensures that we won't see it again for this node via Fisher Yates
            randPeerIndex = numpy.random.randint(0,maxIndices)
            potPeer = nodes[randPeerIndex]
            nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
            maxIndices -= 1

            if potPeer != i and peers[potPeer,i]!=1:
                peersNeededByPeer = p - sum(peers[:,potPeer])
                if peersNeededByPeer > 0:
                    peers[i,potPeer] = 1
                    peers[potPeer,i] = 1
                    peersNeeded-=1
        if peersNeeded > 0:
            return []
    return peers

def getPeerDistFaster(N, p):
    peers = numpy.full((N, p), -1, dtype = int)
    nodes = numpy.arange(N)  # array to randomly shuffle each iteration to give us potential peers in different order
    for i in range(0,N):

        peersNeeded =  p - numpy.count_nonzero(peers[i,:]>=0)

        maxIndices = N-1     #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
        while(peersNeeded > 0 and maxIndices > 0):

            randPeerIndex = numpy.random.randint(0,maxIndices)

            potPeer = nodes[randPeerIndex]

            nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
            maxIndices -= 1

            if potPeer != i and not any(peers[potPeer,:]==i):

                peersNeededByPeer = p - numpy.count_nonzero(peers[potPeer,:] >= 0)
                
                if peersNeededByPeer > 0:
                    peers[potPeer,p - peersNeededByPeer] = i
                    peers[i, p - peersNeeded] = potPeer
                    
                    peersNeeded-=1
        if peersNeeded > 0:
            return []
    return peers

def getPeerDistEvenFaster(N, p):
    peers = numpy.full((N, p), -1, dtype = int)
    nodes = numpy.arange(N)  # array to randomly shuffle each iteration to give us potential peers in different order
    rand = numpy.random.randint
    def peersNeededfunc(n):
        return p - numpy.count_nonzero(peers[n,:] >= 0)
    def findPeersForNode(i,peersNeededfunc,randfunc):
        maxIndices = N-1   #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
        peersNeeded =  peersNeededfunc(i)
    
        while(peersNeeded > 0 and maxIndices > 0):

            randPeerIndex = rand(0,maxIndices)

            potPeer = nodes[randPeerIndex]

            nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
            maxIndices -= 1

            if potPeer != i and not any(peers[potPeer,:]==i):

                peersNeededByPeer = peersNeededfunc(potPeer)
                
                if peersNeededByPeer > 0:
                    peers[potPeer,p - peersNeededByPeer] = i
                    peers[i, p - peersNeeded] = potPeer
                    peersNeeded-=1
        if peersNeeded > 0:
            return True
        else:
            return False
    
    pn = peersNeededfunc
    fvp = findPeersForNode
    if any(fvp(i,pn,rand) for i in range(0,N)):
        yield []
    yield peers

def isValid(peers,N,p):
    if peers == []:
        return False
    b = peers.flatten()
    for i in range(0,N):
        if numpy.count_nonzero(b==i)!=p:
            return False
    return True

def speedTest(N,p,n):
    start = time.time()
    item_start = start
    i = 0
    for item in getPeerDistOrDieTrying(N,p):
        time_now = time.time()
        print("one found in: " + str(time_now - item_start))
        i+=1
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


def getPeerDistFilePath(N,p, s):
    return os.path.normpath(getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(s))

def getProbDistFilePath(N,p, x, i):
    return getFilePathRoot() + '/prob_dist_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i)

def savePeerDist(N,p,x):

    peers = numpy.zeros((N,p))

    for n in range(4, x):
        peers = getPeerDistOrDieTrying(N,p)
        fileName = getPeerDistFilePath(N,p,n)
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








