#ifndef USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7
#define USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7

#include "types.h"

namespace simulation {

    class Ilatency{
        protected:
            using t_t = types::t_t;
            using uid_t = types::uid_t;

        public:
            virtual t_t get_latency(uid_t, uid_t) = 0;
        
        
    };



}

#endif
