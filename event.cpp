#include "event.h"

using simulation::event;

void event::process_event(){
    main_event();
    post_event();
}


