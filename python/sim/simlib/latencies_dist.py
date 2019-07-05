import json
import random
from peer_relationships import peer_dist
import latency_generator 
import latency_cities_generator 



N = 100000
p = 10
start_node_iterations = 10

file_latencies = 'list_town_latencies_pct.txt'

latency_cities_generator.get_latencies_file_name(file_latencies)
'''

#peers = peer_dist.create_peers(N,p,1)
peers = peer_dist.loadPeerDist(N,p,0)



latencies_old = latency_generator.get_latency_relationships(peers)

print(latencies_old)
    
latencies_new = latency_cities_generator.get_latency_relationships(peers)
    
print(latencies_new)
'''
