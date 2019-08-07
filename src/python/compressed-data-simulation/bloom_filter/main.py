from bloomfilter import BloomFilter 
from random import shuffle
import random as rd 
import string
import statistics 
import sys
import math 

len_tx = 10 #Average size of a transaction ~ 250 Bytes = 2000 bits
n = 1000 #no of items to keep
p = 0.0001 #false positive probability
m=5000  #number of participants
r=0.01 #percentage of transactions per participant. l = r*n
b=5 #number of subset per participant. Each subset has r*n/b transactions
s=0.9 #percentage of subsets recieved by each participant. Each participant recieves s*b subset (s*r*n transactions)
n_points = 30 #number of points needed for median/mean 

global_words = []
global_bf = BloomFilter(n,p)
count_words_added = 0
total_words = n*1.0

''' parameters/variables - measurement'''


''' need to make smaller BF somehow for the b subsets to speed the process - Will lose Tx due to FP bit'''

print("=====================================================")
print("***Bloom filter parameters***")
print("False positive Probability: {}".format(global_bf.fp_prob)) 
print("--> Size of bit array: {}".format(global_bf.size)) 
print("Number of hash functions: {}".format(global_bf.hash_count)) 
print("Number of items in Bloom Filter:{} ".format(n)) 
print("Size of items: {}".format(len_tx))
print("=====================================================")
print("***Network parameters***")
print("Number of participants: {}".format(m)) 
print("Number of Tx per participant: {}%".format(r*100)) 
print("Number of subset per participant ({} Tx/subset): {}".format(r*n/b,b)) 
print("Number of subsets collected per participant: {} ({}% of available subsets)".format(s*(m-1)*b,s*100)) 
print("=====================================================")


while count_words_added < n:
    random_string = ''.join([rd.choice(string.ascii_letters + string.digits) for tt in xrange(len_tx)])
    if global_bf.add(random_string,True) == True:
        global_words.append(random_string)
        count_words_added+=1

if len(global_words) != n:
    exit('Not enough items')
    
print("Global Bloom Filter created")
local_bfs=[]
local_words=[]

for it_part in range(m):
    shuffle(global_words)
    wd_part = rd.sample(global_words,int(r*n))
    bin_size = math.floor(len(wd_part)/b)
    wd_part_collect=[]
    bf_part_collect=[]
    for i in range(b-1):
        partial_bf = BloomFilter(n,p)
        range_in = int(bin_size*i)
        range_out = int(bin_size*(i+1))
        wd_part_collect.append(wd_part[range_in:range_out])

        for wd in wd_part[range_in:range_out]:
            partial_bf.add(wd,True)
        bf_part_collect.append(partial_bf)    
            
    wd_part_collect.append(wd_part[range_out:])
    local_words.append(wd_part_collect)

    partial_bf = BloomFilter(n,p)
    for wd in wd_part[range_out:]:
        partial_bf.add(wd,True)
    bf_part_collect.append(partial_bf)
    local_bfs.append(bf_part_collect)
    print("--> Size of bit array: {}".format(partial_bf.size)) 

    #print("Check {}".format(local_words[it_part]))

print("Partial Bloom Filters and Subset of words created")

''' For n_points participant, derive a score of completness'''
''' Turn this into a function - 
for a set (n,m), store the % of nodes collecting 100% Tx 
Ieal: count the number of subset needed to collect 100% Tx for different size of subset --> Define the number of participant OR the level of redundancy '''

completeness_words=[]
for part in range(n_points):
    bf_part = BloomFilter(n,p)
    count_words_part=0
    #print("participant {}".format(part))
    for l_bf in range(len(local_bfs[part])):
         bf_part.mergeQuick(local_bfs[part][l_bf])
    for l_wd in range(len(local_words[part])):
        count_words_part+=len(local_words[part][l_wd])

    #print("counted words: {}".format(count_words_part))
    list_inc_part=[x for x in range(b*part,b*(part+1),1)]
    #print("list_inc_part: {}".format(list_inc_part))
    ''' merge other participants data using BFs. Each participant receives on average s subsets'''

    '''exclude the part'''
    list_s_part=[]
    list_s_part = rd.sample([x for x in range(b*m) if x not in list_inc_part],int(s*b*(m-1)))
    it_4rand = 0
    #print("Getting {} subset".format(len(list_s_part)))
    #print("==> {}".format(list_s_part))
    
    for peer in range(m):
        #print("Peer {}".format(peer))
        if peer == part:
            it_4rand+=b
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
    
