#ifndef USGOV_4fe977c8d0a53583dece022923973911480285192b477133789486114bfa3454
#define USGOV_4fe977c8d0a53583dece022923973911480285192b477133789486114bfa3454

#include "event.h"
#include <vector>
#include "types.h"
#include "message.h"

namespace simulation {

    class message_event : public event {
        
        protected:

            using uid_t = types::uid_t;
            
            message m;
            uid_t from_node_id;
            uid_t to_node_id;
           
        public:
            message_event(t_t time, message m, uid_t from_node_id, uid_t to_node_id): m(m), from_node_id(from_node_id), to_node_id(to_node_id), event(time){};
        

    };

}

#endif
