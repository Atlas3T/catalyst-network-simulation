#include "node_container.h"

using simulation::node_container;

Inodes::get_node_by_id(nid_t node_id){
    return nodes(node_id);
}

std::vector<nid_t> Inodes::get_node_ids(){
   
    vector<nid_t> v;
    for(std::map<nid_t,std::vector<nid_t>>::iterator it = nodes.begin(); it != nodes.end(); ++it) {
        v.push_back(it->first);
    }
    return v;
}

size_t Inodes::get_node_count(){
    return nodes.length();
}


