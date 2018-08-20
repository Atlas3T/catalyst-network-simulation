#ifndef USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7
#define USGOV_69fbab34fea70ccb16a57e86160c797ac1445a3a05061240249e13c321b885c7

#include "types.h"

namespace simulation {

    class Ilatency{
        public:
            virtual types::time_t get_latency(int, int) = 0;
        
    };



}

#endif
