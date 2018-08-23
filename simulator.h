#ifndef USGOV_426a4d8ed8b7e6f41635664f502d988869dce79bc26648d3199fcc9d30c16b40
#define USGOV_426a4d8ed8b7e6f41635664f502d988869dce79bc26648d3199fcc9d30c16b40

#include "schedule.h"
#include "types.h"

namespace simulation{

    class simulator{
        using t_t = types::t_t;
        public:
            simulator(t_t, size_t);
            void run();
        private:
            size_t node_count;
            schedule sched;

    };

}

#endif
