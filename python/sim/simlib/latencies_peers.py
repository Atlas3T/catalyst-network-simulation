import json
import random


def get_latency_relationships(peers):
    
    try:
        #Load cities & percentage 
        cities = []
        percentages = []
        filepath = 'list_town_latencies_pct.txt'      
        with open(filepath) as fp:  
           line = fp.readline()
           while line:
               if line.strip() != '':
                   tmp_strt = line.split('; ')
                   print(tmp_strt)
                   if len(tmp_strt) == 2: 
                       cities.append(tmp_strt[0].strip())
                       percentages.append(float(tmp_strt[1].strip()))
                   else:
                       cities.append(tmp_strt[0].strip())
               line = fp.readline() 
     
        print(cities)

        #add missing percentage for last town 
        if sum(percentages) > 1:
            raise ValueError("Wrong percentage values: sum > 1")
        percentages.append(round(1-sum(percentages),1))

        print(percentages)
        
        #Number of nodes
        N = len(peers[:,0])
        if N%100 != 0:
            raise ValueError("Wrong number of nodes (not a mltiple of 100")

        #Create a list of N city-node bounds
        num_split_nodes = [int(i * N) for i in percentages]
        N_city_index=[]
        it_city_index = 0
        for num_nodes in num_split_nodes:
            N_city_index_part = [it_city_index]*num_nodes
            N_city_index.extend(N_city_index_part)
            it_city_index+=1

        print(N_city_index)                     
        #For each node, for each of its peer draw a random latency

        
        

    
  

    except IOError:
       print("File not found or path is incorrect")
    finally:
       print("------------------")
