#ifndef USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e
#define USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e

#include "Ievent_scheduler.h"
#include "Ilatency.h"
#include <vector>
#include "types.h"

 
namespace simulation{
    
    class network_manager{

        //network manager processes send events and decides which recieve events to create, using info from the Ilatency implementation it has been given.

        using nid_t = simulation::types::nid_t;
        using t_t = simulation::types::t_t;

        public:
            network_manager(Ievent_scheduler & s, Ilatency & l, Inodes & n) : sched(s), latencies(l), nodes(n) {};
            void process_send_event(t_t event_time, std::vector<unsigned char> data, nid_t from_node_id, std::vector<nid_t> to_node_ids);
        private:
            Ievent_scheduler & sched;
            Ilatency & latencies;
            Inodes & nodes;
    };
}

#endif
