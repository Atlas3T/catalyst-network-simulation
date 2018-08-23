#ifndef USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d
#define USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d

#include "message_event.h"
#include "message.h"
#include "types.h"
#include "Inodes.h"
#include "unique_id_generator.h"
#include <vector>

namespace simulation{

    class data_event_manager;
    class recv_event : public message_event {
        using t_t = types::t_t;
        using uid_t = unique_id_generator::uid_t;

        public:
            recv_event(t_t t, message m, uid_t from_node_id, uid_t to_node_id, Inodes & nodes): message_event(t, m, from_node_id, to_node_id), nodes(nodes) {};
        private:
            
            Inodes & nodes;
            void main_event() override;
    };
}

#endif