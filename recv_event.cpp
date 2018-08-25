#include "recv_event.h"
#include <iostream>
#include "node_manager.h"

using simulation::recv_event;

// correct node is found and given necessary info to process the event.

void recv_event::process_event(){
    std::cout << "node " << std::to_string(to_node_id) << "recieving data" << std::endl;
    Inode * node = nodes.get_node_by_id(to_node_id);
    node->process_recieved_data(time, m, from_node_id);
}
