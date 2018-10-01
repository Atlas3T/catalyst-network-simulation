import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
from scipy.special import factorial
from functools import partial
import os.path
import profile
import time

folder = ""

def sendToPeers(peers,messageDist,time):
    p = peers[messageDist == time,:]
    messageDist[p[:]]=numpy.where(messageDist[p[:]]==-1,time+1,messageDist[p[:]])
    return messageDist

def getFilePathRoot(folder):
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/" + str(folder))

def getProbDistFilePath(N,p, x, i):
    return getFilePathRoot() + '/prob_dist_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i)


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








