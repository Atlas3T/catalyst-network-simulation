#ifndef USGOV_e970bcd5b075bee17ebe9e2ac8bca634e77c0bd5fd30042403169a4c345921d1
#define USGOV_e970bcd5b075bee17ebe9e2ac8bca634e77c0bd5fd30042403169a4c345921d1

#include "Ipeers.h"
#include "Inode.h"

namespace simulation {

    class simple_node : public Inode {

        //This is a very simple node which simply recieves data and passes it to its peers (determined by the injected Ipeers implementation) 
        //after a delay. This delay is seperate from the latency delay added by the network manager and could represent processing time.
        
        public:
            simple_node(Ipeers & peers, t_t delay) : peers(peers), delay(delay){};
            void process_recieved_data(types::t_t time, message m, uid_t from_node_id) override;
        private:
            Ipeers & peers;
            t_t delay;
    };

}

#endif

