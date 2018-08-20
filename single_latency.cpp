#include "single_latency.h"

using simulation::single_latency;

simulation::types::time_t single_latency::get_latency(int from_node_id, int to_node_id){
    return 2;
}