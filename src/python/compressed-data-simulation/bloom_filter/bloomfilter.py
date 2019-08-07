# Python 3 program to build Bloom Filter 
# Install mmh3 and bitarray 3rd party module first 
# pip install mmh3 
# pip install bitarray 
import math 
import mmh3 
from bitarray import bitarray 
  
import string

class BloomFilter(object): 
  
    ''' 
    Class for Bloom filter, using murmur3 hash function 
    '''
  
    def __init__(self, items,fp_prob): 
        ''' 
        items_count : int 
            Number of items expected to be stored in bloom filter 
        fp_prob : float 
            False Positive probability in decimal 
        '''
        self.items = items
        
        self.len_items = len(self.items) 

        self.items_count = self.len_items
        
        # False posible probability in decimal 
        self.fp_prob = fp_prob 
  
        # Size of bit array to use 
        self.size = self.get_size(self.items_count,fp_prob) 
  
        # number of hash functions to use 
        self.hash_count = 3 #or self.get_hash_count(self.size,items_count) 
  
        # Bit array of given size 
        self.bit_array = bitarray(self.size) 
  
        # initialize all bits as 0 
        self.bit_array.setall(0)

        
        
        
  
    def add(self, item, unique): 
        ''' 
        Add an item in the filter 
        '''
        digests = []
        count_bit_used = 0

        for i in range(self.hash_count): 
            # create digest for given item. 
            # i work as seed to mmh3.hash() function 
            # With different seed, digest created is different 
            
            digest = mmh3.hash(item,i) % self.size
            
            if self.bit_array[digest] == True:
                #print ("Bit {} (hash {}) already set to 1".format(digest,i))
                count_bit_used+=1
            digests.append(digest)
            # set the bit True in bit_array
        if unique == True:
            if count_bit_used == 0:
                for digest in digests:
                    self.bit_array[digest] = True
                return True
            '''else:
                print("Skipping this word: {} bits set to 1".format(count_bit_used))'''
        else:
            for digest in digests:
                self.bit_array[digest] = True
            return True
        return False

    def mergeQuick(self,bf2):
        '''
        merge two bloom filters quick - no check (no bit counting)
        '''
        self.bit_array = [min(1, x + y) for x, y in zip(self.bit_array, bf2.bit_array)]

        '''for i in range(bf2.size):
            self.bit_array[i] = min(1,self.bit_array[i]+bf2.bit_array[i])'''

    def compare_bitsQuick(self,bf2):
        '''
        compare two bloom filters Quick (no check) (no bit counting)
        '''
        
        different_bits_1 = [(x == y == 1) for x, y in zip(self.bit_array, bf2.bit_array)]
        if any(x == True for x in different_bits_1):
            return False
        return True

    
    def merge(self,bf2):
        '''
        merge two bloom filters (no bit counting)
        '''
        if self.size != bf2.size:
            print("Different BFs size: no comparison possible")
        else:
            for i in range(bf2.size):
                if (bf2.bit_array[i] == 1):
                    self.bit_array[i] = 1


    def compare_bits(self,bf2):
        '''
        compare two bloom filters (no bit counting)
        '''
        if self.size != bf2.size:
            print("Different BFs size: no comparison possible")
            return False
        for i in range(self.size):
            if (self.bit_array[i] == 1 and bf2.bit_array[i] == 1):
                return False
        return True

        
    def check(self, item): 
        ''' 
        Check for existence of an item in filter 
        '''
        for i in range(self.hash_count): 
            digest = mmh3.hash(item,i) % self.size 
            if self.bit_array[digest] == False: 
  
                # if any of bit is False then,its not present 
                # in filter 
                # else there is probability that it exist 
                return False
        return True
   
    
    @classmethod
    def get_size(self,n,p): 
        ''' 
        Return the size of bit array(m) to used using 
        following formula 
        m = -(n * lg(p)) / (lg(2)^2) 
        n : int 
            number of items expected to be stored in filter 
        p : float 
            False Positive probability in decimal 
        '''
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 
  
    @classmethod
    def get_hash_count(self, m, n): 
        ''' 
        Return the hash function(k) to be used using 
        following formula 
        k = (m/n) * lg(2) 
  
        m : int 
            size of bit array 
        n : int 
            number of items expected to be stored in filter 
        '''
        k = (m/n) * math.log(2) 
        return int(k) 