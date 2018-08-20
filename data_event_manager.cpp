#include "data_event_manager.h"

using simulation::data_event_manager;

void data_event_manager::schedule_recv_data(int from_node_id, std::vector<int> to_node_ids, std::vector<unsigned char> data){
    
    for(auto to_node_id : to_node_ids){
        types::time_t latency = latencies.get_latency(from_node_id,to_node_id);
        types::time_t arrival_time = sched.get_time() + latency;
        sched.schedule_event(new recv_data_event(arrival_time, to_node_id, data));
    }
}

void data_event_manager::schedule_recv_data(int from_node_id, std::vector<unsigned char> data){
    
    std::vector<int> to_node_ids = peers.get_peers(from_node_id);
    schedule_recv_data(from_node_id, to_node_ids, data);
    
}