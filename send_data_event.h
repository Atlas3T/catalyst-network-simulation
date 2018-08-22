#ifndef USGOV_3ae556ee756156c22dc921ad6363a5546c4757fa59c6c68785a795980d18197c
#define USGOV_3ae556ee756156c22dc921ad6363a5546c4757fa59c6c68785a795980d18197c

#include "event.h"
#include "network_manager.h"

namespace simulation {

    class send_data_event : public event {
        public:
            send_data_event();
        private:
            void main_event() override;
            network_manager & manager;
    };

}

#endif
