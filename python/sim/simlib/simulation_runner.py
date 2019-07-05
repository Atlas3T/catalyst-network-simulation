from peer_relationships import peer_dist
from peer_relationships import latencies_dist
import propagation_hops
import numpy
import propagation_time
import latency_cities_generator

def run_quick_simulation():
    #1.0 generate file (1 file per case), 10 peers 
    listN = [1000,10000]
    p = 10
    peer_iterations = 1# number of different peer distributions to run simulation over
    start_node_iterations = 3
    #Does not work for other iteration
    listPeers=[]
    for it_N in listN:
        if not peer_dist.verifyFilePath(it_N,p,peer_iterations):
            print("could not find the file {}-{}-{} - Generating it......".format(it_N,p,peer_iterations))
            peer_dist.create_peers(it_N,p,peer_iterations)
            peers_tmp = peer_dist.loadPeerDist(it_N,p,peer_iterations)
            print(peers_tmp)
            listPeers.append(peers_tmp)
        else:
            #load the peers from the exisiting files
            peers_tmp = peer_dist.loadPeerDist(it_N,p,peer_iterations)
            print(peers_tmp)
            listPeers.append(peers_tmp)
            
    #2.0 find the latencies
    file_latencies = 'list1.txt'
    #2.1 generate latencies file name
    filename = latency_cities_generator.get_latencies_filename(file_latencies)

    listLatencies=[]
    #2.2 check if .mat latencies file exit, if not generate
    for it_N in range(len(listN)):
        if not latencies_dist.verifyFilePath(listN[it_N],p,filename):
            print("could not find the file {} - Generating it......".format(filename))
            latencies_tmp = latency_cities_generator.get_latency_relationships(listPeers[it_N],file_latencies)
            print(latencies_tmp)
            listLatencies.append(latencies_tmp)
            latencies_dist.saveLatencyDist(listN[it_N],p,latencies_tmp,filename)
        else:
            #load the latencies from the exisiting files
            latencies_tmp = latencies_dist.loadLatenciesDist(listN[it_N],p,filename)
            print(latencies_tmp)
            listLatencies.append(latencies_tmp)

    print("Up to here - all loaded!")
    listTimeDist=[]
    #3.0 check if .mat time dist file exit, if not generate
    for it_N in range(len(listN)):
        if not propagation_time.isProbDistFile(listN[it_N], p, start_node_iterations,filename):
            print("could not find the file {} - Generating it......".format(filename))
            propagation_time.get_transaction_time_distribution(listN[it_N], p, listPeers[it_N],start_node_iterations,filename,listLatencies[it_N])
            time_dist_tmp = propagation_time.load_transaction_time_distributionBis(listN[it_N], p, start_node_iterations,filename)
            listTimeDist.append(time_dist_tmp[0])
        else:
            time_dist_tmp = propagation_time.load_transaction_time_distributionBis(listN[it_N], p, start_node_iterations,filename)
            #print(time_dist_tmp[0])
            listTimeDist.append(time_dist_tmp[0])
              
    #4.0 Test distribution 
    '''percentage = 0.5
    list = []
    for it_N in range(len(listN)):
        print("==== for {} =====".format(it_N))
        
        dist = listTimeDist[it_N]
        print(dist)
        d = dist.flatten()
        result = numpy.percentile(d,percentage)
        print(result)
        list.append([listN[it_N],result])
    print(list)'''

    for it_N in range(len(listN)):
        test_dist = listTimeDist[it_N]
        print("====")
        print("Network: {} nodes".format(listN[it_N]))
        print("====")
        for i_ms in range(0,500,10):
            result = 0
            for i_d in test_dist:
                if i_d < i_ms:
                    result += 1
                #result = sum(i < i_ms for i in test_dist)
            perc = 1.0
            perc = 100.*result/len(test_dist)
            if perc > 94.9:
                print("{} ms ==> {}".format(i_ms,perc))
                #break
            
'''
def run_simulation():
    listN = [100,1000,10000]
    p = 10
    peer_iterations = 5 # number of different peer distributions to run simulation over
    start_node_iterations = 10
    latency_provider = latency_generator.get_latencies
    #peer_network_provider
    #node_provider
    
    storage_handler = simple_storage.store("/home/engr/Results/sim1")
    
    for N in listN:
        #peer_dist.create_peers(N,p,peer_iterations)   # these don't need to be rerun for each simulation, they have been pre-generated for 5.. and 10..

        propagation_hops.generate_transaction_hop_distribution(N, p, peer_iterations, start_node_iterations, storage_handler)
        propagation_time.generate_transaction_time_distribution(N,p,peer_iterations,start_node_iterations, latency_provider, storage_handler)


    #post_processing
    #create_plots
    '''

if __name__ == '__main__':
    run_quick_simulation()
