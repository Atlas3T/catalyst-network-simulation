#ifndef USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968
#define USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968

#include "Ipeer.h"
#include <random>
#include <map>
#include <vector>

namespace simulation {

    class random_peers : public virtual Ipeer {
        
        public:
            random_peers(size_t node_count, int peer_count) : node_count(node_count), peer_count(peer_count){};
            std::vector<int> get_peers(int node_id);
            int get_random_peer(int node_id);
        private:
            size_t node_count;
            int peer_count;
            std::map<int,std::vector<int>> peers;
            void set_peer_relationships();
            
    };

}

#endif


