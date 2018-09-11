import numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
import os.path
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
        #print(i)
        peersNeeded =  p - numpy.count_nonzero(peers[i,:]>=0)
        #print(peersNeeded)
        maxIndices = N-1     #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
        while(peersNeeded > 0 and maxIndices > 0):
            #print("looking for peer")
            #selects option for peer and ensures that we won't see it again for this node via Fisher Yates
            randPeerIndex = numpy.random.randint(0,maxIndices)
            #print("rand peer index: " + str(randPeerIndex))
            potPeer = nodes[randPeerIndex]
          #  print("rand peer: " + str(potPeer))
            nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
            maxIndices -= 1
            #print(any(peers[potPeer,:]==i))
            if potPeer != i and not any(peers[potPeer,:]==i):
                #print("here")
                #print(peers[potPeer, :])
                #print(peers[potPeer, :] >= 0)
                peersNeededByPeer = p - numpy.count_nonzero(peers[potPeer,:] >= 0)
                #print("pot peer needs " + str(peersNeededByPeer))
                if peersNeededByPeer > 0:
                    peers[potPeer,p - peersNeededByPeer] = i
                    peers[i, p - peersNeeded] = potPeer
                    #print("Found peer")
                    peersNeeded-=1
        if peersNeeded > 0:
            return []
    return peers


def isValid(peers,N,p):
    if peers == []:
        return False
    b = peers.flatten()
    for i in range(0,N):
        if numpy.count_nonzero(b==i)!=p:
            print("invalid")
            return False
    #print(peers)
    return True


def getPeerDistOrDieTrying(N,p):
    i=0
    while(True):
        i+=1
        peers = getPeerDistFaster(N,p)
        if isValid(peers,N,p):
            return peers


def sendToPeers(peers,messageDist,time):
    p = peers[messageDist == time,:]
    messageDist[p[:]]=numpy.where(messageDist[p[:]]==-1,time+1,messageDist[p[:]])
    return messageDist

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/fran/PycharmProjects/PeerDistribution/Results/")


def getPeerDistFilePath(N,p, s):
    return getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(s)

def getProbDistFilePath(N,p, x, i):
    return getFilePathRoot() + '/prob_dist_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i)

def savePeerDist(N,p,x):

    peers = numpy.zeros((N,p))

    for n in range(0, x):
        peers = getPeerDistOrDieTrying(N,p)
        fileName = getPeerDistFilePath(N,p,n)
        scipy.io.savemat(fileName, {"peers" : peers}, appendmat=True)

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








