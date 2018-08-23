#ifndef USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94
#define USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94

#include <vector>
#include <map>
#include "Inode.h"
#include "types.h"

namespace simulation{
    
    class Inodes{
        public:
            std::vector<types::nid_t> get_node_ids();
            Inode get_node_by_id();
            virtual void add_nodes(size_t node_count) = 0;
        private: 
            std::map<nid_t, Inode> nodes;
            
    };
}

#endif