#ifndef USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088
#define USGOV_9c3e92ffffa14a64b388457128284c650147e1e688c19c28c7e97465880af088

#include "event.h"
#include "scheduler.h"
#include "types.h"

namespace simulation{
    
    class sync_event : public event {
        using t_t = types::t_t;
        public:
            sync_event(scheduler & s, t_t t, unsigned int p) : event (t), sched(s), period(p) {};
        protected:
            t_t period;
            scheduler & sched;
            void process_event() override;
    };
}

#endif