#ifndef USGOV_2b958752d6f9e516e215760786938a831ed91807faa25b7de3ffdf2e50e0c873
#define USGOV_2b958752d6f9e516e215760786938a831ed91807faa25b7de3ffdf2e50e0c873

#include "Ilatency.h"
#include "types.h"

namespace simulation{

    class single_latency : public virtual Ilatency{
        public:
            single_latency(){};
            types::time_t get_latency(int from_node_id, int to_node_id);

    };

}

#endif

