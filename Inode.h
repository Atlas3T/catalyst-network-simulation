#ifndef USGOV_4ab53a7ad069fa11c00ffd2d34688a994ddfa92d0fa6ab38ddbdd239c6fead83
#define USGOV_4ab53a7ad069fa11c00ffd2d34688a994ddfa92d0fa6ab38ddbdd239c6fead83

#include "data_event_manager"

namespace simulation {

    class node {

        public:
            nid_t get_id(){return node_id;);
            virtual void process_recieved_data(types::t_t time, std::vector<unsigned char> data, types::nid_t from_node_id) = 0;
            void send_data(std::vector<unsigned char> data, std::vector<types::nid> to_node_ids);
        private:
            data_event_manager & manager;
            nid_t node_id;
    };

}

#endif

