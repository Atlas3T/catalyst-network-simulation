#ifndef USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968
#define USGOV_62a6e0d9bee7fa8b8b1ae9fd817f92c22c728496d1031a525a4de0a5c77b6968

#include "Ipeer.h"
#include "Inodes.h"
#include <random>
#include <map>
#include <vector>
#include "types.h"

namespace simulation {

    class random_peers : public Ipeer {
        using nid_t = types::nid_t;
        public:
            random_peers(Inodes & , size_t);
            std::vector<nid_t> get_peers(nid_t);
            nid_t get_random_peer(nid_t);
        private:
            Inodes & nodes;
            size_t peer_count;
            std::map<nid_t, std::vector<nid_t>> peers;
            void set_peer_relationships();
            
    };

}

#endif


