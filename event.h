#ifndef USGOV_73dbf40b1ac31c28337fdc9f9903bd2c05c669d3b8405af51dbe061f07de7e9c
#define USGOV_73dbf40b1ac31c28337fdc9f9903bd2c05c669d3b8405af51dbe061f07de7e9c

#include "types.h"

namespace simulation{

  class event {
  public:
    
    event (types::time_t t) : time (t)
      { }
    types::time_t time;
    // Execute event by invoking this method.
    void process_event ();

  protected:
    virtual void main_event()=0;
    virtual void post_event()=0;
  };


  struct event_comparator {
    bool operator() (const event * left, const event * right) const {
      return left->time > right->time;
    }
  };

}

#endif