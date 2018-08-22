#include "simulator.h"
#include <iostream>
#include <string>
#include <vector>

//concrete implementations of interfaces
#include "single_latency.h"
#include "random_peers.h"
#include "mock_nodes.h"

using simulation::simulator;
using t_t = simulation::types::t_t;

    simulator::simulator(t_t end_time, size_t node_count) : sched(end_time), node_count(node_count){

    }

    void simulator::run(){
        
        // change concrete implementations here:

        
        //stores nodes. Can use any class that implements Inodes.
        mock_nodes nodes(node_count);
        
        //peer relationships implementation. Can be changed to any concrete class that implements Ipeer.
        size_t peer_count = 8;
        random_peers peers(nodes, peer_count);

        //latency relationships implementation.  Can be changed to any concrete class that implements Ilatency.
        single_latency latency;


        //event_managers
        sync_manager s_manager(sched);
        data_event_manager d_manager(sched, latency, peers);

        s_manager.schedule_initial_events();
        d_manager.schedule_initial_events();

        sched.run();
    }
































