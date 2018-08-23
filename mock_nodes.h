#ifndef USGOV_ca63426abbc857f49cfd59c072f1541f35d641ce4b11e84f02408450085d0a55
#define USGOV_ca63426abbc857f49cfd59c072f1541f35d641ce4b11e84f02408450085d0a55

#include "Inodes.h"
#include "types.h"
#include <vector>

namespace simulation {

    class mock_nodes : public node_container {

        using nid_t = types::nid_t;
        public:
            void add_nodes(size_t) override;
  
    };

}

#endif
