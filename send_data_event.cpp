#include "send_data_event.h"

using simulation::send_data_event;

void send_data_event::main_event(){

    manager.process_send_event(eve)
}