#ifndef USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b
#define USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b

#include <vector>
#include "types.h"

namespace simulation {

    class Ipeer{
        protected:
            using uid_t = types::uid_t;
        public:
            virtual std::vector<uid_t> get_peers(uid_t) = 0;
        
    };

}

#endif