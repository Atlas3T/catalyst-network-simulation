import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
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
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/prob_dist_time_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i))

def loadPeerDist(N,p,n):
        fileName = getPeerDistFilePath(N, p, n)
        contents = scipy.io.loadmat(fileName, appendmat=True)
        peers = contents['peers']
        return peers

def hasMessageSpreadToAllNodes(messageDist):
    return not numpy.any(messageDist==-1)

def disperseMessage(peers,s):
    N = len(peers[:,0])
    messageDist = numpy.full(N,-1, dtype='float')
    latencies = latency_generator.get_latency_relationships(peers)
    #edges are nodes whose peer has already recieved the message.
    edges = numpy.full((N), -1, dtype='float')
    edges[s] = 0
    while (hasMessageSpreadToAllNodes(messageDist)==False):
        
        #records delay for 'edge' node with shortest latency. 
        #We can only 'deliver' one per loop because the new edges may reveal a shorter path.
        edge_value,edge_position = min(((b,a) for a,b in enumerate(edges) if b >= 0))
        messageDist[edge_position]=edge_value
        edges[edge_position]=-1
        #making a fake change
        #peers are new edges
        p=peers[edge_position,:]
        l=latencies[edge_position,:]
        new_values = l[:]+ edge_value
        edges[p[:]] = numpy.where( edges[p[:]] < 0 | (new_values < edges[p[:]]) , new_values, edges[p[:]] ) 
        edges[p[:]] = numpy.where( messageDist[p[:]]==-1, edges[p[:]], -1)

    return messageDist

def saveDisperseMessageDist(N,p,x,iterations):
    delays = []
    for ii in range(0,x):
        peers = loadPeerDist(N,p,ii)
        nodes = numpy.arange(N)
        maxIndices = N-1
        for i in range(0,iterations):
            randStartNodeIndex = numpy.random.randint(0, N-1)
            randNode = nodes[randStartNodeIndex]
            nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
            delays.extend(disperseMessage(peers,randNode))
    results = numpy.array(delays)
    plotDelayDist(results)
    fileName = getProbDistFilePath(N, p, x, iterations)
    scipy.io.savemat(fileName, {"delays": results}, appendmat=True)

def loadPlotDelayDist(N,p,x,iterations):
    delays = loadDisperseMessageDist(N,p,x,iterations)
    plotDelayDist(delays)

def plotDelayDist(delays):
    snsplot = sns.distplot(delays)
    snsplot.figure.savefig(getProbDistFilePath + '_plot.png')

def loadDisperseMessageDist(N,p,x,iterations):

    fileName = getProbDistFilePath(N, p, x, iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    probDist = contents['delays']
    return probDist









