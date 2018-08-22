#ifndef USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94
#define USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94

#include <vector>
#include "types.h"

namespace simulation{
    
    class Inodes{
        public:
            virtual std::vector<types::nid_t> get_node_ids() = 0;
            
    };
}

#endif