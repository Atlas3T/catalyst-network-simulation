#ifndef USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968
#define USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968

#include "Ipeer.h"
#include "node_manager.h"
#include <random>
#include <map>
#include <vector>
#include "types.h"

namespace simulation {

    class random_peers : public Ipeer {
        using uid_t = types::uid_t;
        public:
            random_peers(node_manager & , size_t);
            std::vector<uid_t> get_peers(uid_t) override;
            uid_t get_random_peer(uid_t);
        private:
            node_manager & nodes;
            size_t peer_count;
            std::map<uid_t, std::vector<uid_t>> peers;
            void set_peer_relationships();
            
    };

}

#endif


