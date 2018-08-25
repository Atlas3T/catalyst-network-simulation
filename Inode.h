#ifndef USGOV_4ab53a7ad069fa11c00ffd2d34688a994ddfa92d0fa6ab38ddbdd239c6fead83
#define USGOV_4ab53a7ad069fa11c00ffd2d34688a994ddfa92d0fa6ab38ddbdd239c6fead83

#include "network_manager.h"
#include "message.h"
#include "types.h"
#include <vector>

namespace simulation {

    class Inode {
        protected:
            using uid_t = types::uid_t;
            using t_t = types::t_t;
            
            network_manager & manager;
            uid_t node_id;
        public:
            uid_t get_id(){return node_id;};
            virtual void process_recieved_data(t_t time, message m, uid_t from_node_id) = 0;
            //virtual void send_data(message m, std::vector<uid_t> to_node_ids){};
        
    };

}

#endif

