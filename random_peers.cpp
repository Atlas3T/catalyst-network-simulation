#include "random_peers.h"
#include "algorithm"
#include <array>

using simulation::random_peers;
using namespace std;

void random_peers::set_peer_relationships()
{
    peers.clear();
    map<int, vector<int>> peers;
    // fill array with [min value, max_value] sequence
    array<int, node_count> nodes{};
    iota(nodes.begin(), nodes.end(), 0);

    vector<int> temp_peers;
    for (int i = 0; i < node_count; i++)
    {
        temp_peers = sample nodes.begin(), nodes.end(), temp_peers.begin(), peer_count, std::mt19937{std::random_device{}()});
        peers.insert(pair<int,vector<int>>(i,temp_peers)
    }

}

vector<int> random_peers::get_peers(int node_id)
{
    return peers[node_count];
}

int random_peers::get_random_peer(int node_id)
{
    return 5;
}






