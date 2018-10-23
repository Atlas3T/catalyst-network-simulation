import numpy as numpy
import scipy.io
from numpy.core.multiarray import ndarray
from peer_relationships import peer_dist
import os.path
import time

class propagation_hops:

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.name = 'transaction_hops'

    def get_filename(self, N):
        return self.name + str(N)

    def sendToPeers(self, peers,hops_needed,time):
        p = peers[hops_needed == time,:]
        hops_needed[p[:]]=numpy.where(hops_needed[p[:]]==-1,time+1,hops_needed[p[:]])
        return hops_needed

    def has_transaction_spread_to_all_nodes(self, hops_needed):
        return not numpy.any(hops_needed==-1)

    def relay_single_transaction(self, peers,s):
        N = len(peers[:,0])
        hops_needed = numpy.full(N,-1)
        time = 0
        hops_needed[s] = time
        while (self.has_transaction_spread_to_all_nodes(hops_needed)==False):
            hops_needed = self.sendToPeers(peers,hops_needed,time)
            time += 1
        return hops_needed

    def generate_transaction_hop_distribution(self, N,p,x,iterations_startNode):
        probDist = dict()
        relay_transaction  = self.relay_single_transaction
        numpy_unique = numpy.unique
        for ii in range(0,x):
            peers = peer_dist.loadPeerDist(N,p,ii)
            nodes = numpy.arange(N)
            maxIndices = N-1
            for i in range(0,iterations_startNode):
                randStartNodeIndex = numpy.random.randint(0, N-1)
                randNode = nodes[randStartNodeIndex]
                nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
                hops_needed = relay_transaction(peers,randNode)
                unique_elements, counts_elements = numpy_unique(hops_needed, return_counts=True)
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
        self.file_handler.save_variable(self.name, self.get_filename(N), probs)

    def load_transaction_hop_distribution(N,p,x,iterations_startNode):

        return self.file_handler.load_variable(self.folder_name, get_filename(N))








