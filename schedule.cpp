#include "schedule.h"
#include <iostream>

using simulation::schedule;

void schedule::run () {

  while (! event_queue.empty () && !exit_called) {

    event * next_event = event_queue.top ();
    event_queue.pop ();
    time = next_event->time;
    if(end_time > 0 && time >= end_time){
        break;
    }
    next_event->process_event ();
    delete next_event;
    
  }
}

void schedule::stop(){
    exit_called =true;
}

void schedule::schedule_event( event * new_event) {
            //std::cout << "adding event" << std::endl;
            event_queue.push (new_event);
            //std::cout << "no of events: " << event_queue.size() << std::endl;
}

void schedule::schedule_event(std::vector<event *> new_events) {
            for(auto const& value: new_events) { event_queue.push (value);}
}

simulation::types::time_t schedule::get_time(){
  return time;
}

/* Null, because instance will be initialized on demand. */
