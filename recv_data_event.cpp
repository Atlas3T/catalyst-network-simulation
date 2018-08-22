#include "recv_data_event.h"
#include <iostream>
#include "Inode.h"

using simulation::recv_data_event;

void recv_data_event::main_event(){
    std::cout << "node " << std::to_string(node_id) << "recieving data" << std::endl;
    Inode node = Inodes.get_node_by_id(nid_t node_id);
}

void recv_data_event::post_event(){
    
}