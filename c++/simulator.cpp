#include "simulator.h"

#include <iostream>
#include <string>
#include <vector>

#include "network_manager.h"

//concrete implementations of interfaces
#include "single_latency.h"
#include "random_peers.h"
#include "mock_nodes.h"

#include "sync_event.h"

using simulation::simulator;
using t_t = simulation::types::t_t;

    simulator::simulator(t_t end_time, size_t node_count) : sched(end_time), node_count(node_count){

    }

    void simulator::run(){
        
        // change concrete implementations here:

        
        //stores nodes for lookup by id. Can use any class that implements Inodes.
        mock_nodes nodes;
        nodes.add_nodes(1000);
        
        //peer relationships implementation. Can be changed to any concrete class that implements Ipeer.
        size_t peer_count = 8;
        random_peers peers(nodes, peer_count);

        //latency relationships implementation.  Can be changed to any concrete class that implements Ilatency.
        single_latency latency;

        //initial events happening here for now
        std::vector<t_t> sync_times = {2, 20, 40, 55};  

        for(auto i : sync_times){
            sched.schedule_event(new sync_event(sched, i, 60));   
        } 

        network_manager net_manager(sched, latency);

        sched.run();
    }
































