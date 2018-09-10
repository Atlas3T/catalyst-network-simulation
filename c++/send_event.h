#ifndef USGOV_3ae556ee756156c22dc921ad6363a5546c4757fa59c6c68785a795980d18197c
#define USGOV_3ae556ee756156c22dc921ad6363a5546c4757fa59c6c68785a795980d18197c

#include "message_event.h"
#include "types.h"
#include <vector>
#include "network_manager.h"

namespace simulation {

    class send_event : public message_event {
        
        public:
            send_event(t_t t, message m, uid_t from_node_id, std::vector<uid_t> to_node_ids, network_manager * nm): message_event(t, m, from_node_id,to_node_ids) {net_manager = nm;};
        private:
            void process_event() override;
            network_manager * net_manager;
            
    };
}

#endif
