#include "sync_event.h"
#include <iostream>

using simulation::sync_event;

void sync_event::main_event(){
        std::cout << "sync now " << std::to_string(time) << std::endl;
    }

void sync_event::post_event(){
    
    sched.schedule_event(new sync_event(sched, time+period, period));
}
