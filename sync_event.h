#ifndef USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088
#define USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088

#include "event.h"
#include "Ievent_scheduler.h"
#include "types.h"

namespace simulation{
    class Ievent_manager;
    class sync_event : public event {
        using t_t = types::t_t;
        public:
            sync_event(t_t t, Ievent_scheduler & s, unsigned int p) : event (t), sched(s), period(p) {};
        protected:
            t_t period;
            Ievent_scheduler & sched;
            void main_event();
            void post_event();
    };
}

#endif