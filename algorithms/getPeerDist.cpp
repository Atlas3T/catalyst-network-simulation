
#include <vector>
using std::vector;

vector<vector<int>>  getPeerDistFaster(int N, int p){

    vector<vector<int>> peer_dist = vector<vector<int>>(N,p);
    vector<int> nodes = vector<int>(N,p);
    nodes = numpy.arange(N)  # array to randomly shuffle each iteration to give us potential peers in different order
    for i in range(0,N):

        peersNeeded =  p - numpy.count_nonzero(peers[i,:])
        maxIndices = N-1     #Using as part of Fisher-Yates algorithm to provide unique random options for peers efficiently.
        while(peersNeeded > 0 and maxIndices > 0):

            //selects option for peer and ensures that we won't see it again for this node via Fisher Yates
            randPeerIndex = numpy.random.randint(0,maxIndices)
            potPeer = nodes[randPeerIndex]
            nodes[maxIndices], nodes[randPeerIndex] = nodes[randPeerIndex], nodes[maxIndices]
            maxIndices -= 1

            if potPeer != i and not any(peers[potPeer,:]==i):
                peersNeededByPeer = p - numpy.count_nonzero(peers[potPeer,:])
                if peersNeededByPeer > 0:
                    peers[potPeer,p - peersNeededByPeer] = i
                    peers[i, p - peersNeeded] = potPeer
                    peersNeeded-=1
        if peersNeeded > 0:
            return []
    return peers
}