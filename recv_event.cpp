#include "recv_data_event.h"
#include <iostream>
#include "Inode.h"

using simulation::recv_data_event;

// correct node is found and given necessary info to process the event.

void recv_event::main_event(){
    std::cout << "node " << std::to_string(to_node_id) << "recieving data" << std::endl;
    Inode node = Inodes.get_node_by_id(uid_t node_id);
    node.process_recieved_data(time,data,from_node_id);
}
