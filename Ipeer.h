#ifndef USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b
#define USGOV_bf3b7774d74e8403aa0f747315cdce869f8822179797d9b5069591f3952f669b

#include <vector>

namespace simulation {

    class Ipeer{
        public:
            virtual std::vector<int> get_peers(int) = 0;
        
    };

}

#endif