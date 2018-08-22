#include "random_peers.h"
#include <algorithm>
#include <array>
#include <random>

using simulation::random_peers;
using namespace std;
using nid_t = simulation::types::nid_t;

random_peers::random_peers(Inodes & nodes, size_t peer_count) : nodes(nodes), peer_count(peer_count){
    set_peer_relationships();
}

void random_peers::set_peer_relationships()
{
    vector<nid_t> node_ids = nodes.get_node_ids();
    peers.clear();

    size_t node_count = size(node_ids);
    vector<nid_t> temp_peers;

    for (size_t i = 0; i < node_count; i++)
    {
        sample(node_ids.begin(), node_ids.end(), std::back_inserter(temp_peers), peer_count, std::default_random_engine{std::random_device{}()});
        peers.insert(make_pair(node_ids[i],temp_peers));
    }

}

vector<nid_t> random_peers::get_peers(nid_t node_id){
    return peers[node_id];
}

nid_t random_peers::get_random_peer(nid_t node_id)
{
    return 5;
}






