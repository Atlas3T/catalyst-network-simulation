#include "simulator.h"
#include <iostream>
#include <string>
#include <vector>


using simulation::simulator;

    simulator::simulator(types::time_t et, int nc) : sched(et), node_count(nc){

        sync_manager s_manager(sched);
        s_manager.schedule_initial_events();
        single_latency latencies;
        random_peers peers(node_count, 8);
        data_event_manager de_manager(sched, latencies, peers);

    }

    void simulator::run(){
        
        sched.run();
    }
































