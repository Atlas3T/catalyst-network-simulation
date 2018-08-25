#include "sync_event.h"
#include <iostream>

using simulation::sync_event;

void sync_event::process_event(){
        std::cout << "sync now " << std::to_string(time) << std::endl;
        sched.schedule_event(new sync_event(sched, time+period, period));
    }

