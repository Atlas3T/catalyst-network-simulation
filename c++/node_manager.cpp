#include "node_manager.h"

using simulation::node_manager;

simulation::Inode* node_manager::get_node_by_id(uid_t node_id){
    return nodes(node_id);
}

std::vector<uid_t> node_manager::get_node_ids(){
   
    std::vector<uid_t> v;
    for(std::map<uid_t,Inode>::iterator it = nodes.begin(); it != nodes.end(); ++it) {
        v.push_back(it->first);
    }
    return v;
}

size_t node_manager::get_node_count(){
    return nodes.size();
}


