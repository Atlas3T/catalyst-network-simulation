#ifndef USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088
#define USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088

#include "event.h"
#include "Ievent_scheduler.h"

namespace simulation{
    class sync_event : public event {
        public:
            sync_event(Ievent_scheduler & s, types::time_t t, unsigned int p) : event (t), sched(s), period(p) {};
        protected:
            types::time_t period;
            Ievent_scheduler & sched;
            void main_event();
            void post_event();
    };
}

#endif