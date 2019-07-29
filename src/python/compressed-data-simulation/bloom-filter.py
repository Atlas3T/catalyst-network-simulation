import pybloom_live as pbl
#  from compression import compress_object


def create_bloom_filter():
    bloom_filter = pbl.BloomFilter(10000,error_rate=0.001)
    [bloom_filter.add(x) for x in range(1000)]
    test = int(bloom_filter.bitarray)
    print(test)

 

    return(bloom_filter())

bloom_filter = create_bloom_filter()
#int_bloom_filter = int(bloom_filter)
#compression.compress_object(int_bloom_filter)