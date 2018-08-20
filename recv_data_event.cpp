#include "recv_data_event.h"
#include <iostream>

using simulation::recv_data_event;

void recv_data_event::main_event(){
    std::cout << "node " << std::to_string(node_id) << "recieving data" << std::endl;
}