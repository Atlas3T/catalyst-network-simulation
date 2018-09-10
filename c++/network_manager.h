#ifndef USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e
#define USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e

#include "scheduler.h"
#include "Ilatency.h"
#include <vector>
#include "types.h"
#include "message.h"

namespace simulation{
    
    class network_manager{

        //network manager processes send events and decides which recieve events to create, using info from the Ilatency implementation it has been given.

        using uid_t = types::uid_t;
        using t_t = types::t_t;

        public:
            network_manager(scheduler & s, Ilatency & l) : sched(s), latencies(l) {};
            void process_send_event(t_t event_time, message m, uid_t from_node_id, std::vector<uid_t> to_node_ids);
        private:
            scheduler & sched;
            Ilatency & latencies;
    };
}

#endif
