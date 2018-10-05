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
import peer_dist
from heapq import heappush, heappop
from functools import reduce
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

def getProbDistFilePath(N,p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/prob_dist_time_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i))

def getProfileSetTimePath(time ,p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/profile_set_time_' + str(time)+ '_' + str(p) + "_" + str(x)+ "_" + str(i))

def getProfileSetPercentPath(percent, p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/profile_set_percent_' + str(percent) + '_' + str(p) + "_" + str(x)+ "_" + str(i))


def hasMessageSpreadToAllNodes(messageDist):
    return not numpy.any(messageDist==-1)

def disperseMessage(peers,s):
    N = len(peers[:,0])
    messageDist = numpy.full(N,-1, dtype='float')
    latencies = latency_generator.get_latency_relationships(peers)
    #edges are nodes whose peer has already recieved the message.

    #edges = numpy.full((N), -1, dtype='float')
    #edges[s] = 0
    heap = []
    heappush(heap, (0,s))
    nodes_reached_count = 0
    while (nodes_reached_count<N):
        
        #records delay for 'edge' node with shortest latency. 
        #We can only 'deliver' one per loop because the new edges may reveal a shorter path.
        
        #edge_value,edge_position = min(((b,a) for a,b in enumerate(edges) if b >= 0))
        edge_latency,edge_no = heappop(heap)
        if messageDist[edge_no]==-1:
            messageDist[edge_no]=edge_latency
            nodes_reached_count+=1

            #edges[edge_position]=-1
            
            #peers are new edges
            new_edges=peers[edge_no,:]
            l=latencies[edge_no,:]
            new_values = l[:]+ edge_latency
            #edges[p[:]] = numpy.where( edges[p[:]] < 0 | (new_values < edges[p[:]]) , new_values, edges[p[:]] ) 
            #edges[p[:]] = numpy.where( messageDist[p[:]]==-1, edges[p[:]], -1) #where peer not already contacted
            for it, edge in enumerate(new_edges):
                if messageDist[edge]==-1:
                    heappush(heap,(new_values[it],edge)) 
    if(hasMessageSpreadToAllNodes(messageDist)!=True):
        print("invalid: transaction hasn't spread to all nodes!")
        print(messageDist)
    return messageDist

def saveDisperseMessageDist(N,p,x,iterations):
    delays = numpy.zeros((x,iterations,N),dtype=int)
    for ii in range(0,x):
        peers = peer_dist.loadPeerDist(N,p,ii)
        nodes = numpy.arange(N)
        maxIndices = N-1
        for i in range(0,iterations):
            randStartNodeIndex = numpy.random.randint(0, N-1)
            randNode = nodes[randStartNodeIndex]
            nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
            delays[ii,i,:]=disperseMessage(peers,randNode)
    results = delays.flatten()
    fileName = getProbDistFilePath(N, p, x, iterations)
    scipy.io.savemat(fileName, {"delays": results}, appendmat=True)


def loadDisperseMessageDist(N,p,x,iterations):

    fileName = getProbDistFilePath(N, p, x, iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    probDist = contents['delays']
    return probDist

def profile_max(listofN,p,x,iterations):
    list = []

    for N in listofN:
        dist = loadDisperseMessageDist(N,p,x,iterations)
        m = max(dist.flatten())
        list.append ([N,m])
    print(list)

def percentage_under_cuttoff_latency(listofN,p,x,iterations,ms):
    #list = load_p_u_c_l(ms,p,x,iterations)
    list = []
    for N in listofN:
        dist = loadDisperseMessageDist(N,p,x,iterations)
        d = dist.flatten()
        no_under = numpy.count_nonzero(d < ms)
        result = no_under/len(d)
        list.append ([N,result])
    fileName = getProfileSetTimePath(ms,p,x,iterations)
    scipy.io.savemat(fileName, {"profile": list}, appendmat=True)
    print(list)

def latency_at_cuttoff_percentage(listofN,p,x,iterations,percentage):
    #list = load_l_a_c_p(percentage,p,x,iterations)
    list=[]
    for N in listofN:
        dist = loadDisperseMessageDist(N,p,x,iterations)
        d = dist.flatten()
        result = numpy.percentile(d,percentage)
        list.append([N,result])
    fileName = getProfileSetPercentPath(percentage,p,x,iterations)
    scipy.io.savemat(fileName, {"profile": list}, appendmat=True)
    print(list)

def load_p_u_c_l(ms,p,x,iterations):
    fileName = getProfileSetTimePath(ms,p,x,iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    list = contents['profile']
    return list.tolist()

def load_l_a_c_p(percentage,p,x,iterations):
    fileName = getProfileSetPercentPath(percentage,p,x,iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    list = contents['profile']
    return list.tolist()






