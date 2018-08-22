#ifndef USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d
#define USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d

#include "event.h"
#include "types.h"
#include "Inodes.h"
#include <vector>

namespace simulation{

    class data_event_manager;
    class recv_data_event : public event {
        using t_t = types::t_t;
        using nid_t = types::nid_t;

        public:
            recv_data_event(t_t t, nid_t from_node_id, nid_t to_node_id, std::vector<unsigned char> data): event(t), node_id(node_id), data(data){};
        private:
            std::vector<unsigned char> data;
            Inodes & nodes;
            nid_t from_node_id;
            nid_t to_node_id;
            data_event_manager * manager;
            void main_event() override;
    };
}

#endif