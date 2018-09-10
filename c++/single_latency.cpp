#include "single_latency.h"

using simulation::single_latency;

using t_t = simulation::types::t_t;
using uid_t = simulation::types::uid_t;

t_t single_latency::get_latency(uid_t from_node_id, uid_t to_node_id){
    return 2;
}