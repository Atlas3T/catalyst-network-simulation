import json
import random
import string
import scipy.stats
import numpy

def deleteMS( str ):
   b = "ms"
   for char in b:
       str = str.replace(char,"")   
   return str

def get_latency_rvs(M, mu, lower, upper,sigma):
    #print("factors: {}, {}, {}, {}, {}".format(M, mu, lower, upper,sigma))
    return scipy.stats.truncnorm.rvs(
        (lower-mu)/sigma ,(upper-mu)/sigma,loc=mu,scale=sigma,size=M)


def get_latencies_filename(filepath):
    try:
        #Load cities & percentage 
        cities = []
        percentages = []
             
        with open(filepath) as fp:  
           line = fp.readline()
           while line:
               if line.strip() != '':
                   tmp_strt = line.split('; ')
                   #print(tmp_strt)
                   if len(tmp_strt) == 2: 
                       cities.append(tmp_strt[0].strip())
                       percentages.append(float(tmp_strt[1].strip()))
                   else:
                       cities.append(tmp_strt[0].strip())
               line = fp.readline() 
     

        if sum(percentages) > 1:
            raise ValueError("Wrong percentage values: sum > 1")
        percentages.append(round(1-sum(percentages),1))

        filename = ''
        for it in range(len(cities)):
            filename+=cities[it]
            filename+=str(percentages[it])
            filename+='-'
        filename = filename[0:len(filename)-1]
        #print(filename)
        return filename
            
    except IOError:
       print("File not found or path is incorrect")
    finally:
       print("------------------")
       
def get_latency_relationships(peers,filepath):
    
    try:
        #Load cities & percentage 
        cities = []
        percentages = []
             
        with open(filepath) as fp:  
           line = fp.readline()
           while line:
               if line.strip() != '':
                   tmp_strt = line.split('; ')
                   #print(tmp_strt)
                   if len(tmp_strt) == 2: 
                       cities.append(tmp_strt[0].strip())
                       percentages.append(float(tmp_strt[1].strip()))
                   else:
                       cities.append(tmp_strt[0].strip())
               line = fp.readline() 
        
        #print(cities)
        dataset_towns = []
        #Load the JSON files
        for city in cities:
            path_json_file = "../../git-data/JSON/"
            path_json_file += city
            path_json_file += ".json"
            dataset_towns.append(json.loads(open(path_json_file).read()))

        #Create a matrix of latency parameter for town1/town2 pairs
        num_city = 0
        city_lat_avg_typ = 6
        cities_lat_avg_set = [] 
        city_lat_min_typ = 5
        cities_lat_min_set = [] 
        city_lat_max_typ = 30
        cities_lat_max_set = [] 
        city_lat_dev_typ = 2
        cities_lat_dev_set = [] 
        for city in cities:
            city_lat_avg_set = []
            city_lat_min_set = []
            city_lat_max_set = []
            city_lat_dev_set = []
            for city2 in cities:
                city_lat_avg = 0
                city_lat_min = 0
                city_lat_nmax = 0
                city_lat_dev = 0
                if city != city2:
                    for it_city in dataset_towns[num_city]:
                        if it_city['City'] == city2:
                            city_lat_avg = int(float(deleteMS(it_city['Average'])))
                            city_lat_avg_set.append(city_lat_avg)
                            city_lat_min = int(float(deleteMS(it_city['min'])))
                            city_lat_min_set.append(city_lat_min)
                            city_lat_max = int(float(deleteMS(it_city['max'])))
                            city_lat_max_set.append(city_lat_max)
                            city_lat_dev = float(deleteMS(it_city['mdev'] )) * 1.47
                            city_lat_dev_set.append(city_lat_dev)
                else:
                    city_lat_avg_set.append(city_lat_avg_typ)  
                    city_lat_min_set.append(city_lat_min_typ)  
                    city_lat_max_set.append(city_lat_max_typ)  
                    city_lat_dev_set.append(city_lat_dev_typ)
                    
            cities_lat_avg_set.append(city_lat_avg_set)
            cities_lat_min_set.append(city_lat_min_set)
            cities_lat_max_set.append(city_lat_max_set)
            cities_lat_dev_set.append(city_lat_dev_set)
            num_city += 1
        
        #print("The Average latency per twon pair {}".format(cities_lat_avg_set))
        
        #add missing percentage for last town 
        if sum(percentages) > 1:
            raise ValueError("Wrong percentage values: sum > 1")
        percentages.append(round(1-sum(percentages),1))

        #print(percentages)
        
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

        #print(N_city_index)

        #Create a flow latencies vector and initialise
        p = len(peers[0,:])
        M=N*p
        samples = [0]*M
        latencies_all = numpy.reshape(samples,(N,p))
        #print("test {}".format(latencies_all[N-1][p-1]))
        #print("2nd peer of first node ? {} ".format(peers[0][1]))
        #For each node, for each of its peer draw a random latency
        for i_node in range(N):
            index_node1 = i_node
            #print("===========================")
            for i_peer in range(p):
                index_node2 = peers[i_node,i_peer]
                
                town_1 = N_city_index[index_node1]
                town_2 = N_city_index[index_node2]
                #With the index get the average (to do replace with random draw)
                avg_temp = cities_lat_avg_set[town_1][town_2]
                min_temp = cities_lat_min_set[town_1][town_2]
                max_temp = cities_lat_max_set[town_1][town_2]
                dev_temp = cities_lat_dev_set[town_1][town_2]
                if dev_temp < 1:
                   dev_temp = 1
                   max_temp += 1
                   min_temp -= 1
                
                lat_temp = get_latency_rvs(1,avg_temp,min_temp,max_temp,dev_temp)
                
                #print("Node {} / peer {} : {} & {} --> {} ms".format(i_node,index_node2,town_1,town_2,lat_temp))     
                latencies_all[i_node][i_peer] = lat_temp
                
            
        #print(latencies_null)
        
        return latencies_all
        

    
  

    except IOError:
       print("File not found or path is incorrect")
    finally:
       print("------------------")
