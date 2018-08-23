#include "send_data_event.h"

using simulation::send_data_event;

void send_data_event::main_event(){

    net_manager->process_send_event(time, data, from_node_id, to_node_id);
}