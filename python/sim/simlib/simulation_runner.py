from peer_relationships import peer_dist
import propagation_hops 
import propagation_time
from storage import simple_storage
import latency_generator

def run_simulation():
    listN = [100,1000,10000]
    p = 10
    peer_iterations = 5 # number of different peer distributions to run simulation over
    start_node_iterations = 10
    
    file_handler = simple_storage.store("/home/engr/Results/sim1")
    
    for N in listN:
        #peer_dist.create_peers(N,p,peer_iterations)   # these don't need to be rerun for each simulation, they have been pregenerated for 5.. and 10..

        propagation_hops.generate_transaction_hop_distribution(N, p, peer_iterations, start_node_iterations, file_handler)
        propagation_time.generate_transaction_time_distribution(N,p,peer_iterations,start_node_iterations, latency_generator, file_handler)

    

if __name__ == '__main__':
    run_simulation()
    