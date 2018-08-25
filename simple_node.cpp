#include "simple_node.h"
#include "send_event.h"


using simulation::simple_node;
using uid_t = simulation::types::uid_t;
using t_t = simulation::types::t_t;

void simple_node::process_recieved_data(t_t time, message m, uid_t from_node_id){

    //Node gets list of its peers.
    std::vector<uid_t> my_peers = peers.get_peers(node_id);

    //creates a send data event after delay.
    types::t_t processing_time = 1;
    sched.schedule_event(new send_event(time + processing_time, m, id, my_peers));

}