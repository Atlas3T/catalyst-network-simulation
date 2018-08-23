#include "mock_nodes.h"

using simulation::mock_nodes;
using nid_t = simulation::types::nid_t;

std::vector<nid_t> mock_nodes::add_nodes(size_t node_count){

    for(int i = 0; i< node_count; i++){
        nid_t next_id = nodes.length();
        nodes.insert(make_pair(next_id, new simple_node()))
    }
    
    return node_ids;
}

