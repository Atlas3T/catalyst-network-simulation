#ifndef USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d
#define USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d

#include "message_event.h"
#include "message.h"
#include "types.h"
#include "node_manager.h"
#include <vector>
#include "Inode.h"

namespace simulation{

    class data_event_manager;
    class recv_event : public message_event {
        
        public:
            recv_event(t_t t, message m, uid_t from_node_id, std::vector<uid_t> to_node_ids, node_manager & nodes): message_event(t, m, from_node_id, to_node_ids), nodes(nodes) {};
        private:
            
            node_manager & nodes;
            void process_event() override;
    };
}

#endif