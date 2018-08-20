#ifndef USGOV_426a4d8ed8b7e6f41635664f502d988869dce79bc26648d3199fcc9d30c16b40
#define USGOV_426a4d8ed8b7e6f41635664f502d988869dce79bc26648d3199fcc9d30c16b40

#include "schedule.h"
#include "single_latency.h"
#include "data_event_manager.h"
#include "sync_manager.h"
#include "types.h"
#include "random_peers.h"

namespace simulation{

    
    class simulator{
        public:
            simulator(types::time_t, int);
            void run();
        private:
            int node_count;
            schedule sched;
            single_latency latency;

    };

}

#endif
