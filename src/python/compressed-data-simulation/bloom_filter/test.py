from bloomfilter import BloomFilter 
from random import shuffle
import random as rd 
import string
import statistics 
import sys
import math 

len_tx = 10 #Average size of a transaction ~ 250 Bytes = 2000 bits
producer_ids = range(10, 111)
list_producer_ids = []
for i in producer_ids:
    list_producer_ids.append(i) #no of items to keep
prob_false_posative = 0.0000001 #false positive probability
size_of_bitarray=10000  #number of participants
percent_transactions_per_participant=0.01 #percentage of transactions per participant. l = r*n
subsets_per_participant=5 #number of subset per participant. Each subset has r*n/b transactions
subsets_recieved=0.9 #percentage of subsets recieved by each participant. Each participant recieves s*b subset (s*r*n transactions)
n_points = 30 #number of points needed for median/mean 
correct_producer_ratio = 0.7
num_correct_prod = int(correct_producer_ratio * len(list_producer_ids))

correct_producers = rd.sample(list_producer_ids,num_correct_prod)
print (correct_producers)
global_words = []
global_bf = BloomFilter(list_producer_ids,prob_false_posative)
count_words_added = 0
total_words = len(list_producer_ids)*1.0

print("=====================================================")
print("***Bloom filter parameters***")
print("False positive Probability: {}".format(global_bf.fp_prob)) 
print("--> Size of bit array: {}".format(global_bf.size)) 
print("Number of hash functions: {}".format(global_bf.hash_count)) 
print("Number of items in Bloom Filter:{} ".format(len(list_producer_ids))) 
print("Size of items: {}".format(len_tx))
print("=====================================================")

for prod in list_producer_ids:
    prod2 = bytes(prod)
    if global_bf.add(prod2, False) == True:
        global_words.append(prod)
        count_words_added+=1

if len(global_words) != len(list_producer_ids):
    exit('Not enough items')
    
print("Global Bloom Filter created")

local_bfs=[]
local_words=[]
list_of_bfs = []
#At this point the global bloom filter is created. This is the bloom filter that all others will be compared too

for all_prod in list_producer_ids: 
    
    for corr_prod in correct_producers:
        local_bf = BloomFilter(list_producer_ids,prob_false_posative)
        prod = bytes(corr_prod)
        if local_bf.add(prod, False) == True:
            global_words.append(corr_prod)
            count_words_added+=1
        list_of_bfs.append(local_bf)
print(len(list_of_bfs))
print(list_of_bfs())

for it_part in range(size_of_bitarray):
    shuffle(global_words)
    wd_part = rd.sample(global_words,int(percent_transactions_per_participant*len(list_producer_ids)))
    bin_size = math.floor(len(wd_part)/subsets_per_participant)
    wd_part_collect=[]
    bf_part_collect=[]
    for i in range(subsets_per_participant-1):
        partial_bf = BloomFilter(list_producer_ids,prob_false_posative)
        range_in = int(bin_size*i)
        range_out = int(bin_size*(i+1))
        wd_part_collect.append(wd_part[range_in:range_out])

        for wd in wd_part[range_in:range_out]:
            partial_bf.add(wd,True)
        bf_part_collect.append(partial_bf)    
            
    wd_part_collect.append(wd_part[range_out:])
    local_words.append(wd_part_collect)

    partial_bf = BloomFilter(list_producer_ids,prob_false_posative)
    for wd in wd_part[range_out:]:
        wd = bytes(wd)
        partial_bf.add(wd,True)
    bf_part_collect.append(partial_bf)
    local_bfs.append(bf_part_collect)


    completeness_words=[]
for part in range(n_points):
    bf_part = BloomFilter(list_producer_ids,prob_false_posative)
    count_words_part=0
    #print("participant {}".format(part))
    for l_bf in range(len(local_bfs[part])):
         bf_part.mergeQuick(local_bfs[part][l_bf])
    for l_wd in range(len(local_words[part])):
        count_words_part+=len(local_words[part][l_wd])

    #print("counted words: {}".format(count_words_part))
    list_inc_part=[x for x in range(subsets_per_participant*part,subsets_per_participant*(part+1),1)]
    #print("list_inc_part: {}".format(list_inc_part))
    ''' merge other participants data using BFs. Each participant receives on average s subsets'''

    '''exclude the part'''
    list_s_part=[]
    list_s_part = rd.sample([x for x in range(subsets_per_participant*size_of_bitarray) if x not in list_inc_part],int(subsets_recieved*subsets_per_participant*(size_of_bitarray-1)))
    it_4rand = 0
    #print("Getting {} subset".format(len(list_s_part)))
    #print("==> {}".format(list_s_part))
    
    for peer in range(size_of_bitarray):
        #print("Peer {}".format(peer))
        if peer == part:
            it_4rand+=subsets_per_participant
            #print("it_rand pat = {}".format(it_4rand))
            continue
        for l_bf_peer in range(len(local_bfs[peer])):
            it_4rand += 1
            #print("it_rand = {}".format(it_4rand))
            if it_4rand in list_s_part:
                '''improve count'''
                #print("merging {} - [{}][{}]".format(it_4rand,peer,l_bf_peer))
                if bf_part.compare_bitsQuick(local_bfs[peer][l_bf_peer]) == True:
                    bf_part.mergeQuick(local_bfs[peer][l_bf_peer])
                    count_words_part+=len(local_words[peer][l_bf_peer])
                #print("counted words: {} ==> {}".format(len(local_words[peer][l_bf_peer]),count_words_part))
                
    ''' store accounted words '''
    completeness_words.append(count_words_part)
    print("counted words: {}".format(count_words_part))

print("================================")
print("median of missing words: {}".format((total_words-statistics.median(completeness_words))/total_words))
print("mean of missing words: {}".format((total_words-statistics.mean(completeness_words))/total_words))
print("================================")