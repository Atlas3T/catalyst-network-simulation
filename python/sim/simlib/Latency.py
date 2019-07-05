import json
import string
import random 
import time
import numpy
import scipy.stats
import matplotlib.pyplot as plt
import math
import sys


def deleteMS( str ):
   b = "ms"
   for char in b:
       str = str.replace(char,"")   
   return str

def deleteKM( str ):
   b = "kms"
   for char in b:
       str = str.replace(char,"")
       
   return str

def get_latency_rvs(M, mu, lower, upper,sigma):
    return scipy.stats.truncnorm.rvs(
        (lower-mu)/sigma ,(upper-mu)/sigma,loc=mu,scale=sigma,size=M)
    



try:
    count_subplots = 1
    for i in range (0,4):
        # 1.- list of cities to test
        cities = ['London', 'Adelade','Paris','Moscow','Aukland','Barcelona','Budapest','Cardiff','Cincinnati','Copenhagen','Detroit','Dublin','Ho Chi Minh City','Hanoi','Hong Kong''Lisbon','Los Angeles','Madrid','Manchester','Miami','New Delhi','Pittsburgh','Quito','Pune','Sapporo','Shanghai','Zhangjiakou','Wellington','Vladivostok']
        # 2.- Create two nodes and rdm associate a town (to mean randomly select two towns for 1 dist)
        town1 = random.choice(cities)
        cities.remove(town1)
        town2 = random.choice(cities)
     
        print("Towns selected for rdm draw: {} and {}".format(town1,town2))
        #3.- Load the dataset of town1
        
        path_json_file = "../../../JSON/"
        path_json_file += town1
        path_json_file += ".json"
        dataset_town1 = json.loads(open(path_json_file).read())
        #4.- Extract parameters for destination town2
        min_lat = 0
        max_lat = 0
        avg_lat = 0
        mdev_lat = 0
            #If statment needed for if town 2 not in dataset of town 1
        for it_town in dataset_town1:
            if it_town['City'] == town2:
                avg_lat = int(float(deleteMS(it_town['Average'])))
                min_lat = int(float(deleteMS(it_town['min'])))
                max_lat = int(float(deleteMS(it_town['max'])))
                mdev_lat =float(deleteMS(it_town['mdev'] )) * 1.47
                dist = it_town['Distance']
                print("Average: {}".format(avg_lat))
        if min_lat == max_lat:
            max_lat += 1
   
        if mdev_lat == 0:
            print("No Dev")
            continue
   
   

  
       
   #5.- Loop over N = 1000 times, each time, randomly select from a dist using above parameters
   #print every 10 iterations
     
    
        Ndraw = 1000

        plt.suptitle('Latency distribution',fontsize=13)
        lat_draws = get_latency_rvs(Ndraw,avg_lat, min_lat,max_lat,mdev_lat)
        ax = plt.subplot(2,2,count_subplots)
        '''if count_subplots == 1:
            plt.subplot(2,2,count_subplots)
        elif count_subplots == 2:
            plt.subplot(2,2)
        elif count_subplots == 3:
            plt.subplot(1,1)
        elif count_subplots == 4:
            plt.subplot(1,2)'''
        maxbin = int(1.1*lat_draws.max())
        minbin = int(0.9*lat_draws.min())
        bins = numpy.linspace(minbin, maxbin,200)
        ax.set_title(town1 +' to '+town2 + ' ' + dist, fontsize=8, fontweight='bold')
        plt.tight_layout()
        #plt.suptitle(town1 +' to '+town2, fontsize=8, fontweight='bold')
        plt.xlabel('Latency (ms)',fontsize=8)
        
        plt.ylabel('Frequency',fontsize=8)
        plt.hist(lat_draws, bins, alpha=0.5, histtype='bar', ec='green')
        if all(lat_draws > 300):
            plt.hist(lat_draws, bins, alpha=0.5, histtype='bar', ec='red')
        elif any(lat_draws > 300):
            plt.hist(lat_draws, bins, alpha=0.5, histtype='bar', ec='orange')
            
        plt.xticks(fontsize = 8) 
        plt.yticks(fontsize = 8)
        textstr = '\n'.join((
        #r'$\min=%.2f$' % (int(min_lat), ),
        #r'$\max=%.2f$' % (max_lat, ),
        
        r'$\sigma (ms)=%.0f$' % (mdev_lat , ),
        r'$avg (ms)=%.0f$' % (avg_lat , )))
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.65, 0.95, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
        #plt.text(avg_lat, (min_lat+max_lat)/2, textstr, fontsize=14, verticalalignment='top', bbox=props)
        count_subplots += 1
    
    plt.show()
  

except IOError:
   print("File not found or path is incorrect")
finally:
   print("------------------")