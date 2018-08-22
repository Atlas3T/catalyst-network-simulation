#include "Inode.h"

using simulation::Inode;

void Inode::send_data(std::vector<unsigned char> data, std::vector<types::nid> to_node_ids){
    manager.schedule_recv_data(node_id, to_node_ids,data);
}