#ifndef USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d
#define USGOV_97a4cf1e0b6a7c076fc6e248e82e4f91d6a63c48fd28388868e198187b69875d

#include "event.h"
#include "types.h"
#include <vector>

namespace simulation{

    class recv_data_event : public event {
        public:
            recv_data_event(types::time_t t, int node_id, std::vector<unsigned char> data): event(t), node_id(node_id), data(data) {};
        private:
            std::vector<unsigned char> data;
            int node_id;
            void main_event();
            void post_event(){};
    };
}

#endif