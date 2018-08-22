#include "network_manager.h"
#include "Ievent_scheduler.h"

using simulation::network_manager;
using nid_t = simulation::types::nid_t;
using t_t = simulation::types::t_t;

void network_manager::process_send_event(t_t event_time, nid_t from_node_id, std::vector<nid_t> to_node_ids, std::vector<unsigned char> data){
    for(auto to_node_id : to_node_ids){
        t_t latency = latencies.get_latency(from_node_id,to_node_id);
        t_t arrival_time = sched.get_time() + latency;
        sched.schedule_event(new recv_data_event(arrival_time, to_node_id, data));
    }
}
