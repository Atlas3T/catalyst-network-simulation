import numpy
import scipy.io
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
    print(peers)
    return True


def getPeerDistOrDieTrying(N,p):
    i=0
    while(True):
        i+=1
        peers = getPeerDistFaster(N,p)
        if isValid(peers,N,p):
            return peers


def sendToPeers(peers,messageDist,time):
    print("messsage dist:")
    #print(messageDist)
    sentTo = numpy.multiply(messageDist,peers)
    #print("sent to")
    #print(sentTo)
    x = numpy.nonzero(sentTo)
    nor = x[0]
    #print(nor)
    for p in nor:
        if messageDist[p] == 0:
            messageDist[p] = time

    return messageDist

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/fran/PycharmProjects/PeerDistribution/Results/")


def getPeerDistFilePath(N,p, s):
    return getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(s)

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
    return not numpy.any(messageDist==0)

def disperseMessage(peers,s):
    N = len(peers[:,1])
    messageDist = numpy.zeros(N)
    time = 1
    messageDist[s] = time
    while (hasMessageSpreadToAllNodes(messageDist)==False):
        time+=1
        messageDist=sendToPeers(peers,messageDist,time)
    return messageDist






