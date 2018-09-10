#ifndef USGOV_81a0979085acbe2a5e2616be12860aaa4e9d31fa9973291933fe90e480e4010e
#define USGOV_81a0979085acbe2a5e2616be12860aaa4e9d31fa9973291933fe90e480e4010e

namespace simulation{

    class unique_id_generator {
    public:
        using uid_t = unsigned int;
        static unique_id_generator * instance ();
        uid_t next () { return _id++; }
    private:
        unique_id_generator () : _id(0) {}

        static unique_id_generator * only_copy;
        uid_t _id;
    };

}

#endif

