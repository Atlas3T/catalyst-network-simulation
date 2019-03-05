#produce the raw data files
import generate_peers
import generate_latencies
import generate_propagation
import generate_postprocessed_files
import generate_graphs


import numpy as np
from numpy import median

def run_simu_test():

    listN = [10000,50000] 
    p = 10   
    f_lat = 'list1.txt'
    lat_name = generate_latencies.getFilename(f_lat)

    ################ start_node_iterations sets the number of transactions that are sent############
    ################ If you are looking at PUCL and LAPC then it should be set to 1 ###############
    ################ as it will slow the program down with very little gain ##############
   
    start_node_iterations = 10000
    
    
    ################## Outputs ########################
    listPeers=[]
    listLatencies=[]
    listPropTimes=[]
    listAvgTimes=[]
    listMedTimes=[]

    
    ################## Load the peers ##################
    for iN in listN:
        peers_tmp = generate_peers.get_peers(iN,p)
        #print("Size of peer {}".format(len(peers_tmp[:,0])))
        listPeers.append(peers_tmp)
    print("peers generated...")

    ############ For the latencies the default levels (where c1 = c2) can be found in ##################
    ############ sim/simlib/localData.txt ############


    for it_N in range(len(listN)):
        lats_tmp = generate_latencies.get_lats(listN[it_N],p,listPeers[it_N],f_lat)
        listLatencies.append(lats_tmp)
    print("latencies generated...")
    
    
    ####################### Load the simulation files ###########################

    for it_N in range(len(listN)):
        prop_tmp, avg_tmp, med_tmp = generate_propagation.get_propagation_and_average(listN[it_N],p,listPeers[it_N],listLatencies[it_N],lat_name,start_node_iterations)
        
        listAvgTimes = avg_tmp[0]
        listMedTimes = med_tmp[0]
        listPropTimes.append(prop_tmp)
        
        print(listAvgTimes)
    print("propagations generated...")
    
    ###################### Generate list of 0-5 and 95-100 percentiles ################################
    
    testPercentile = np.percentile(listAvgTimes, 95)
    testPercentile2 = np.percentile(listAvgTimes, 5)
    ninetyFivePercentiles = [i for i in listAvgTimes if i >= testPercentile]
    fivePercentiles = [i for i in listAvgTimes if i <= testPercentile2]   
  

    print()
    print("average test : {}".format(median(listMedTimes)))
    if len(listN) == 1:
        print ("Function to be added for distribution curves")
        

        generate_graphs.plot_Median_distribution(listMedTimes,start_node_iterations)
        print("Averages generated...")

    else:
        print("Too many sets of nodes to give an accurate average reading")    

    if len(listN) == 1:
        print ("Function to be added for distribution curves")
        
        #for it_N in range(len(listAvgTimes)):
            #quick_Average = listAvg(listN[it_N],p,listPeers[it_N],listLatencies[it_N],f_lat,start_node_iterations)
        generate_graphs.plot_Average_distribution(listAvgTimes,start_node_iterations,ninetyFivePercentiles,fivePercentiles),

        print("Averages generated...")

    else:
        print("Too many sets of nodes to give an accurate average reading")
    
   
################ This will only run if there is more than three network sizes availiable as ###############
################ graph will be pointless otherwise  ##########


    if len(listN) >= 3:

        ms = 650
        PUCL_140 = generate_postprocessed_files.get_p_u_c_l(listN,p,listPropTimes,lat_name,ms)
        print("post-processed data generated...")
        generate_graphs.plot_profile_set_latency(ms,PUCL_140,listN,p)
 
        percentage = 95
        LACP_85 = generate_postprocessed_files.get_l_a_c_p(listN,p,listPropTimes,lat_name,percentage) 
        print("LACP data generated")
        generate_graphs.plot_latency_set_prob(percentage,LACP_85,listN,p)
    else:
        print ("Not enough values to give an accurate graph for PUCL or LACP")

def run_quick_simulation():
    
    ############### These are input parameters, ListN is the size of the network, #########################
    ############### set multiple networks to see PUCL and LAPC, set to one for multiple ###################
    ############### transaction distributions. f_lat is where the txt file containing #################
    ############## the cities being observed is kept. p is the nuber of peers assigned  ####################
    ############### for each node. To be accurate the p value should be kept low as the ############
    ############### no. of hops will reduce is the value for p is increased on a small network #################################

    listN = [1000,2000,3000,5000,10000,15000,25000,50000,100000] 
    p = 3   
    f_lat = 'list1.txt'
    lat_name = generate_latencies.getFilename(f_lat)

    ################ start_node_iterations sets the number of transactions that are sent############
    ################ If you are looking at PUCL and LAPC then it should be set to 1 ###############
    ################ as it will slow the program down with very little gain ##############
   
    start_node_iterations = 1 
    
    
    ################## Outputs ########################
    listPeers=[]
    listLatencies=[]
    listPropTimes=[]

    
    ################## Load the peers ##################
    for iN in listN:
        peers_tmp = generate_peers.get_peers(iN,p)
        #print("Size of peer {}".format(len(peers_tmp[:,0])))
        listPeers.append(peers_tmp)
    print("peers generated...")

    ############ For the latencies the default levels (where c1 = c2) can be found in ##################
    ############ sim/simlib/localData.txt ############


    for it_N in range(len(listN)):
        lats_tmp = generate_latencies.get_lats(listN[it_N],p,listPeers[it_N],f_lat)
        listLatencies.append(lats_tmp)
    print("latencies generated...")
    
    
    ####################### Load the simulation files ###########################

    for it_N in range(len(listN)):
        prop_tmp = generate_propagation.get_propagations(listN[it_N],p,listPeers[it_N],listLatencies[it_N],lat_name,start_node_iterations)
        listPropTimes.append(prop_tmp)
    print("propagations generated...")
   
    
    #################### Function needed for generating the distribution curves ################

    if len(listN) == 1:
        print ("Function to be added for distribution curves")


        for it_N in range(len(listN)):
            #quick_Average = generate_propagation.get_Quick_Average(listN[it_N],p,listPeers[it_N],listLatencies[it_N],f_lat,start_node_iterations)
            generate_graphs.plot_distribution(quick_Average,start_node_iterations)
            print("Averages generated...")

    else:
        print("Too many sets of nodes to give an accurate average reading")

    
################ This will only run if there is more than three network sizes availiable as ###############
################ graph will be pointless otherwise  ##########


    if len(listN) >= 3:

        ms = 650
        PUCL_140 = generate_postprocessed_files.get_p_u_c_l(listN,p,listPropTimes,lat_name,ms)
        print("post-processed data generated...")
        generate_graphs.plot_profile_set_latency(ms,PUCL_140,listN,p)
 
        percentage = 95
        LACP_85 = generate_postprocessed_files.get_l_a_c_p(listN,p,listPropTimes,lat_name,percentage) 
        print("LACP data generated")
        generate_graphs.plot_latency_set_prob(percentage,LACP_85,listN,p)
    else:
        print ("Not enough values to give an accurate graph for PUCL or LACP")




if __name__ == '__main__':
    #run_quick_simulation()
    run_simu_test()