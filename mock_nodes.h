#ifndef USGOV_ca63426abbc857f49cfd59c072f1541f35d641ce4b11e84f02408450085d0a55
#define USGOV_ca63426abbc857f49cfd59c072f1541f35d641ce4b11e84f02408450085d0a55

#include "Inodes.h"
#include "types.h"
#include <vector>

namespace simulation {

    class mock_nodes : public Inodes {

        using nid_t = types::nid_t;
        public:
            mock_nodes(size_t node_count) : node_count(node_count){};
            std::vector<nid_t> get_node_ids() override;

            private:
                size_t node_count;
    };

}

#endif
