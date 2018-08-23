#ifndef USGOV_d67d2b565aafaafd52ad08e29115893f33b66f5f6829d5b9fb9ac1e30653e7c8
#define USGOV_d67d2b565aafaafd52ad08e29115893f33b66f5f6829d5b9fb9ac1e30653e7c8

#include "unique_id_generator.h"
#include <vector>

namespace simulation {

    class message {
        using uid_t = unique_id_generator::uid_t;
        public:
            message(){id=unique_id_generator::instance()->next();}
            uid_t get_id(){return id;}
            std::vector<unsigned char> get_data(){return data;};
        private:
            uid_t id;
            std::vector<unsigned char> data;

    };

}

#endif


