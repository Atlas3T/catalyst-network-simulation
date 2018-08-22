#ifndef USGOV_187bcf8f1f6c911b8c74b24801fc323161dcc9f717d5ef62b2924a636f80930a
#define USGOV_187bcf8f1f6c911b8c74b24801fc323161dcc9f717d5ef62b2924a636f80930a

#include "event.h"
#include "types.h"

namespace simulation{

    class Ievent_scheduler{

        public:
            virtual void schedule_event(event*) = 0;
            virtual types::t_t get_time() = 0;
            
    };
}

#endif