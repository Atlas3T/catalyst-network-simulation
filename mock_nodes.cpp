#include "mock_nodes.h"
#include <numeric>

using simulation::mock_nodes;
using nid_t = simulation::types::nid_t;

std::vector<nid_t> mock_nodes::get_node_ids(){

    nid_t first_id =1;
    std::vector<nid_t> node_ids(node_count);
    std::iota(node_ids.begin(), node_ids.end(), first_id);
    return node_ids;
}

