#include "scheduler.h"
#include <iostream>

using simulation::scheduler;
using t_t = simulation::scheduler::t_t;

void scheduler::run () {

  while (! event_queue.empty () && !exit_called) {

    event * next_event = event_queue.top ();
    event_queue.pop ();
    time = next_event->time;
    next_event->process_event ();
    delete next_event;
    
  }
}

void scheduler::stop(){
    exit_called =true;
}

void scheduler::schedule_event( event * new_event) {
            //std::cout << "adding event" << std::endl;
            if(new_event->time < end_time){
              event_queue.push (new_event);
            }
            //std::cout << "no of events: " << event_queue.size() << std::endl;
}

void scheduler::schedule_event(std::vector<event *> new_events) {
            for(auto const& new_event: new_events) { schedule_event(new_event);}
}

t_t scheduler::get_time(){
  return time;
}

/* Null, because instance will be initialized on demand. */
