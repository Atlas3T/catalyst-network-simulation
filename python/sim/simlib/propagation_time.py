import numpy
import scipy.io
import os.path
from heapq import heappush, heappop
from peer_relationships import peer_dist
import latency_generator

def getFilePathRoot():
    return os.path.expanduser("~/local-data/")

def getProbDistFilePath(N,p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/prob_dist_time_' + str(N) + '_' + str(p) + "_" + str(x)+ "_" + str(i))

def has_message_spread_to_all_nodes(nodes_recieved_message):
    return not numpy.any(nodes_recieved_message==-1)

def relay_single_transaction(peers,start_node):
    """
    Relays a transaction through the peer network.

    as nodes recieve the transaction, their peers are added to the upcoming_events collection
    to allow the transaction to be relayed in the correct order. The transaction is relayed until all nodes 
    have recieved it.

    Parameters
    ----------
    peers : array
        Array containing the peers of each node
    start_node : int
        start_node is the node where the transaction originates

    Returns
    -------
    float array
        Array of times taken for nodes to recieve transaction. Node number is index, value is time taken.

    """
    
    N = len(peers[:,0])

    #array of time that each node recieved transaction. -1 if node has not yet recieved it.
    time_recieved = numpy.full(N,-1, dtype='float')
    latencies = latency_generator.get_latency_relationships(peers)
    
    upcoming_events = []

    #using heapq package for quick 'popping' of next event
    heappush(upcoming_events, (0,start_node))
    nodes_reached_count = 0
    while (nodes_reached_count<N):
        
        #while loop delivers transaction (records delay in time_recieved) for 'edge' node with shortest latency in upcoming_events.  Transaction has now been recieved by that node.
        #We can only 'deliver' one per loop because the new edges may reveal a shorter path.
        
        time_taken,current_node = heappop(upcoming_events)
        if time_recieved[current_node]==-1:
            
            time_recieved[current_node]=time_taken
            nodes_reached_count+=1

            #peers are new edges
            new_edge_nodes=peers[current_node,:]
            l=latencies[current_node,:]
            new_time_values = l[:]+ time_taken

            for it, edge_node in enumerate(new_edge_nodes):
                #only add to upcoming_events if peer has not yet recieved transaction
                if time_recieved[edge_node]==-1:
                    heappush(upcoming_events,(new_time_values[it],edge_node)) 
    if(has_message_spread_to_all_nodes(time_recieved)!=True):
        print("invalid: transaction hasn't spread to all nodes!")
        print(time_recieved)
    return time_recieved

def generate_transaction_time_distribution(N:int, p:int, peer_iterations: int, start_node_iterations: int):
    """
    Generates and saves transaction relay times for dispering a transaction to the network. Saved to .mat file.

    Parameters
    ----------
    N : int
        Number of nodes in network
    p : str
        Number of peers for each node
    peer_iterations : int
        number of different peer distributions to iterate simulation over. !!!Should be moved outside of function and each run saved seperately!!
    start_node_iterations : int
        number of different starting nodes to iterate simulation over. !!!Should be moved outside of function and each run saved seperately!!
    
    """
    delays = numpy.zeros((peer_iterations,start_node_iterations,N),dtype=int)
    for i_p in range(0,peer_iterations):
        peers = peer_dist.loadPeerDist(N,p,i_p)
        nodes = numpy.arange(N)
        maxIndices = N-1
        for i_s in range(0,start_node_iterations):
            
            #chooses a random starting node using Yates-Fisher algorithm for speed
            randStartNodeIndex = numpy.random.randint(0, N-1)
            randNode = nodes[randStartNodeIndex]
            nodes[maxIndices], nodes[randStartNodeIndex] = nodes[randStartNodeIndex], nodes[maxIndices]
            
            delays[i_p,i_s,:]=relay_single_transaction(peers,randNode)

    results = delays.flatten()

    fileName = getProbDistFilePath(N, p, peer_iterations, start_node_iterations)
    scipy.io.savemat(fileName, {"delays": results}, appendmat=True)


def load_transaction_time_distribution(N,p,x,iterations):

    fileName = getProbDistFilePath(N, p, x, iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    probDist = contents['delays']
    return probDist








