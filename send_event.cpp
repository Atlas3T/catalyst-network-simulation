#include "send_event.h"

using simulation::send_event;

void send_event::process_event(){

    net_manager->process_send_event(time, m, from_node_id, to_node_id);
}