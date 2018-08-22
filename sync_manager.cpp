#include "sync_manager.h"

#include "sync_event.h"
#include "Ievent_scheduler.h"
#include <iterator>

using simulation::sync_manager;

    void sync_manager::schedule_initial_events(){

            for(auto i : sync_times){
                sched.schedule_event(new sync_event(sched, i, sync_period));   
            }   
    }

   


