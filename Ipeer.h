#ifndef USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b
#define USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b

#include <vector>
#include "types.h"

namespace simulation {

    class Ipeer{
        using nid_t = types::nid_t;
        public:
            virtual std::vector<nid_t> get_peers(nid_t) = 0;
        
    };

}

#endif