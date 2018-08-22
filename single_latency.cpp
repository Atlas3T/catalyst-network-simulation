#include "single_latency.h"

using simulation::single_latency;
using t_t = simulation::types::t_t;
using nid_t = simulation::types::nid_t;

t_t single_latency::get_latency(nid_t from_node_id, nid_t to_node_id){
    return 2;
}