#ifndef USGOV_d913bee82d6bee9f81ff71e04504b36bcba297d915df474f77edb74f3820b9d4
#define USGOV_d913bee82d6bee9f81ff71e04504b36bcba297d915df474f77edb74f3820b9d4

#include <vector>
#include "Ievent_scheduler.h"
#include "Ievent_manager.h"
#include "types.h"

namespace simulation{
    class sync_manager : Ievent_manager{
        using t_t = types::t_t;
        
        public:
        sync_manager (Ievent_scheduler & s) : sched(s){};
        void schedule_initial_events() override;

        private:
            Ievent_scheduler & sched;
            t_t sync_period = 60;  
            std::vector<t_t> sync_times = {2, 20, 59, 55};  


    };
}

#endif