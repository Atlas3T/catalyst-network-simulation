#include "simple_node.h"
#include "send_data_event.h"


using simulation::simple_node;

void simple_node::process_recieved_data(types::t_t time, std::vector<unsigned char> data, types::nid_t from_node_id){

    //Node gets list of its peers.
    std::vector<nid_t> peers_of_node = peers.get_peers(node_id);

    //creates a send data event after delay.
    types::t_t processing_time = 1;
    sched.schedule_event(new send_data_event(time + processing_time, data, ))

}