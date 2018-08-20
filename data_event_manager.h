#ifndef USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e
#define USGOV_62389406d6682a464ead65b68c70edb95f6efd90098f34105d836b40addee64e

#include "Ievent_scheduler.h"
#include "Ilatency.h"
#include "Ipeer.h"
#include "recv_data_event.h"
#include <vector>
#include "types.h"

namespace simulation{
    
    class data_event_manager{
        public:
            data_event_manager(Ievent_scheduler & s, Ilatency & l, Ipeer & p) : sched(s), latencies(l), peers(p){};
            void schedule_recv_data(int from_node_id, std::vector<int> to_node_ids, std::vector<unsigned char> data);
            void schedule_recv_data(int from_node_id, std::vector<unsigned char> data);
        private:
            Ievent_scheduler & sched;
            Ilatency & latencies;
            Ipeer & peers;
    };
}

#endif
