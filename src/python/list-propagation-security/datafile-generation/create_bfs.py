from bloomfilter import BloomFilter 
import random as rd 
import numpy as np
import math
from itertools import chain



def generate_bf_lists(num_producers, num_collected_candidates):
    list_ids = np.zeros((num_producers, num_collected_candidates),int)

    for i in range(num_producers):
        list_ids[i,0] = i
        list_ids[i,1:num_collected_candidates] =  rd.sample(list(chain(range(0, i), range(i + 1, num_producers))), num_collected_candidates - 1)
    
    return list_ids


def create_list_of_bfs(producers_id, prob_false_positive, num_collected_quantities, correct_producers_id):
    producers_bf = []
    
    for i in producers_id:
        collected_quantities_bf = BloomFilter(producers_id, prob_false_positive)
        collected_quantities_id = rd.sample(producers_id,num_collected_quantities)
        for j in collected_quantities_id:
            if j in correct_producers_id:
                corr_prod = bytes(j)
                collected_quantities_bf.add(corr_prod, False)
        producers_bf.append(collected_quantities_bf)
    return producers_bf


def create_output(P, producers_id, producers_list_of_bfs, producers_bf, num_collected_candidates, correct_producers_id):
    producer_bf_threshold = num_collected_candidates/2
    num_outputs = 2 
    # For each producer, number of producers found from Cn within merged BF, 
    # and number of producers not from Cn
    
    output = np.zeros((P, num_outputs), int)
    
    for i in producers_id: #For each producer
        count_ids_in_cn = 0
        count_ids_out_cn = 0
        for k in producers_id:
            counter = 0
            for j in (producers_list_of_bfs[i,:]): 
                #print(producers_list_of_bfs[i,:])
                producers_bloom = producers_bf[j]
                producer_id_bytes = bytes(k)
                if producers_bloom.check(producer_id_bytes) == True:
                    counter +=1
            if counter >= producer_bf_threshold:
                if k in correct_producers_id:
                    count_ids_in_cn += 1
                else:
                    count_ids_out_cn += 1
        output[i,0] = count_ids_in_cn
        output[i,1] = count_ids_out_cn
    return output

#1. Total number of producers and various proportion, variables declaration



#2. Step1 : for each produer, create a temp bloomfilter
# only append to the bloom filterm the id of producer from Cn i < num_correct_producers
# add bloomfilter to producers_bf


def create_bfs(producers_id, prob_false_positive, num_collected_quantities, total_no_prod, num_collected_candidates, num_correct_producers):
    
    
    correct_producers_id = [i for i in range(0, num_correct_producers)]
    
    producers_bf = []
    producers_bf = create_list_of_bfs(producers_id, 
                                      prob_false_positive, 
                                      num_collected_quantities, correct_producers_id)


    #3. Step 2 : create (within a def) the matrix  producers_list_of_bfs: for each i in P, 
    # create a random list of num_collected_candidates value between 0 and P
    # Look into get_list_producer_ids in get_lists.py

    producers_list_of_bfs = generate_bf_lists(total_no_prod, 
                                              num_collected_candidates)

    #4. Step 3 : fill the output matrix:
    # For each i in P,
    #       count_ids_in_cn = 0
    #       count_ids_out_cn = 0
    #       For each j in P
    #           Check in how many bfs from producers_list_of_bfs[i,:] j is found
    #           If appears more than threshold, then:
    #             if j in Cn : count_ids_in_cn ++
    #             else count_ids_out_cn ++
    #      output.append(count_ids_in_cn, count_ids_out_cn)
       

    output = create_output(total_no_prod, producers_id, 
                           producers_list_of_bfs, producers_bf, num_collected_candidates, correct_producers_id)


    return (output)
    
