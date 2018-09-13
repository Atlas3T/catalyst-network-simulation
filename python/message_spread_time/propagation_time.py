import numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
import os.path
import latency_generator
numpy.set_printoptions(threshold=numpy.inf)


def sendToPeers(peers,messageDist,time):
    ends = peers[messageDist == time,:]
    print('ends')
    print(ends)
    messageDist[ends[:]]=numpy.where(messageDist[ends[:]]==-1,time+1,messageDist[ends[:]])
    return messageDist

def getFilePathRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/")


def getPeerDistFilePath(N,p, s):
    return os.path.normpath(getFilePathRoot() + '/peer_dist_' + str(N) + '_' + str(p) + "_" + str(s))

def getProbDistFilePath(N,p, x, i):
    return os.path.normpath(getFilePathRoot() + '/Prob_dist_time/prob_dist_time_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i))

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
    messageDist[s] = 0
    latencies = latency_generator.get_latency_relationships(peers)
    edges = numpy.full((N), -1)
    edges[s] = 0
    while (hasMessageSpreadToAllNodes(messageDist)==False):
        value,position = min(((b,a) for a,b in enumerate(edges) if b>=0))
        print('position')
        print(position)
        messageDist[position]=value
        edges[position]=0
        print('ends')
        print(edges)
        p=peers[position,:]
        print(p)
        l=latencies[position,:]
        print(l)
        edges[p[:]] = numpy.where(edges[p[:]] >= 0 and l[:] + value < edges[p[:]],l[:],edges[p[:]])
        
    return messageDist

def saveDisperseMessageDist(N,p,x,iterations_startNode):
    probDist = dict()
    delays = []
    for ii in range(0,x):
        peers = loadPeerDist(N,p,ii)
        nodes = numpy.arange(N)
        maxIndices = N-1
        for i in range(0,iterations_startNode):
            randStartNodeIndex = numpy.random.randint(0, N-1)
            randNode = nodes[randStartNodeIndex]
            nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
            numpy.append(delays,disperseMessage(peers,randNode))
            
    fileName = getProbDistFilePath(N, p, x, iterations_startNode)
    scipy.io.savemat(fileName, {"probDist": delays}, appendmat=True)
    print(delays)

def loadDisperseMessageDist(N,p,x,iterations_startNode):

    fileName = getProbDistFilePath(N, p, x, iterations_startNode)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    probDist = contents['probDist']
    return probDist








