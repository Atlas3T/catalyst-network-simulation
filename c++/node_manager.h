#ifndef USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94
#define USGOV_505b83511e3a21bb39930568176bee9029784a86db7c636eb518a11f5dcece94

#include <vector>
#include <map>
#include "Inode.h"
#include "types.h"

namespace simulation{
    
    class node_manager{
        public:
            std::vector<types::uid_t> get_node_ids();
            Inode * get_node_by_id(uid_t);
            virtual void add_nodes(size_t node_count) = 0;
            size_t get_node_count();
        private: 
            std::map<uid_t, Inode> nodes;      
    };
}

#endif