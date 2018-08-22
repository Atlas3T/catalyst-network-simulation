#ifndef USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7
#define USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7

#include "types.h"

namespace simulation {

    class Ilatency{
        using t_t = types::t_t;
        using nid_t = types::nid_t;

        public:
            virtual t_t get_latency(nid_t, nid_t) = 0;
        
        
    };



}

#endif
