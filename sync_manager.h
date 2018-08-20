#ifndef USGOV_d913bee82d6bee9f81ff71e04504b36bcba297d915df474f77edb74f3820b9d4
#define USGOV_d913bee82d6bee9f81ff71e04504b36bcba297d915df474f77edb74f3820b9d4

#include <vector>
#include "Ievent_scheduler.h"
#include "types.h"

namespace simulation{
    class sync_manager {
        public:
        sync_manager (Ievent_scheduler & s) : sched(s) {};
        void schedule_initial_events();

        private:
            Ievent_scheduler & sched;
            unsigned int sync_period = 60;  
             std::vector<types::time_t> sync_times = {2, 20, 59, 55};     
    };
}

#endif