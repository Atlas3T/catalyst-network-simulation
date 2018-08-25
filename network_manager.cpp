#include "network_manager.h"
#include "recv_event.h"

using simulation::network_manager;
using uid_t = simulation::types::uid_t;
using t_t = simulation::types::t_t;

void network_manager::process_send_event(t_t event_time, message m, uid_t from_node_id, std::vector<uid_t> to_node_ids){
    for(auto to_node_id : to_node_ids){
        t_t latency = latencies.get_latency(from_node_id,to_node_id);
        t_t arrival_time = sched.get_time() + latency;
        //sched.schedule_event(new recv_event(arrival_time, data, from_node_id, to_node_id, nodes));
    }
}
