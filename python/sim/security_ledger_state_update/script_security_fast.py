import numpy
import random
import math


def does_simulated_consensus_produce_correct_ln(P, ProportionProducersSameDelta, ProportionOfDeltaCollected,
                                                ProportionProducersRecieveVote, ProportionProducersRecieveFinalVote):

    #K_n = NumDeltasSame: number of producers amongst P that generate the correct (dominant) ledger state update
    #L_prod: list of K_n
    #Typically 50%P < K_n < P [0.55,0.99]
    ###Computation phase###
    
    NumDeltasSame=math.floor(ProportionProducersSameDelta*P)
    
    #IDs_prod: index is producer, value 1 if produces correct delta, 0 otherwise
    IDs_prod = numpy.zeros(P,int)
    IDs_prod[:NumDeltasSame] = 1  #1 1 1 1 1 .. 0 0 0 0 0
    #L_prod is list of producers we want to be agreed at the end (list of producers who shoulqa`d recieve reward-1)
    L_prod = [i for i in range(NumDeltasSame)] #1 2 3 4 5 6 ... K_n
    
    ###Voting phase 1#### (creation of L_j(prod) 
    #K_j = NumDeltasCollected: number of h_k collected by a producer P_j
    #NumDeltasCollected: a common K_j for any producer P_j
    #K_j > K_min and (K^maj > K_threshold =? K^maj/K_j)
    NumDeltasCollected=math.floor(ProportionOfDeltaCollected*P) #each producer P_j collected K_j NumDeltasCollected deltas in mempool during phase 1
    K_min = math.floor(NumDeltasCollected*0.5)  #that is 50% of collected data, in reality K_min should depends on K_j and NumDeltasCollected > K_min
    #V_n = NumVotesSame: number of producers amongst P that generate the correct (dominant) vote
    #L_vote: list of V_n
    L_vote = []
    #P_IDs, each row contains index of which producer's deltas have been collected by each producer
    #NOTE, producers should not be able to collect their delta, but should necessarily have their own delta 
    P_IDs = numpy.zeros((P,NumDeltasCollected),int)
    for i in range(P):
        P_IDs[i,:]=random.sample(range(P),NumDeltasCollected)
    #lj_prod = each row contains index of producers that P believes to have produced the most common delta, otherwise -1.
    #lj_prod may certainly not be a complete representation of the list L_n(prod)
    lj_prod=numpy.zeros((P,NumDeltasCollected),int)
    #v = each row contains 1 if the producer believes he found a common delta, 0 otherwise
    v=numpy.zeros((P), int)
    for i in range(P):
        #Question: Is it true that K^maj = numpy.count_nonzero(D[P_IDs[i,:]]==1)?
        v[i]=1 if numpy.count_nonzero(IDs_prod[P_IDs[i,:]]==1) > K_min else 0
        if v[i] == 1: #P_i found the correct common delta
           L_vote.append(i)
           for j in range(NumDeltasCollected):
            if IDs_prod[P_IDs[i,j]]==1:
                lj_prod[i,j] = P_IDs[i,j]
            else:
                lj_prod[i,j] = -1
        else:
            lj_prod[i,:] = -1

    ####Voting phase 2### merge the L_k(prod) to create L_n(prod) which should include all the producers K_n
    #Only if P_j has produced the right ledger state update, said otherwise P_j included in K_n
    #V_j : number of v_k collected by a producer P_j
    #NumVotesCollected: a common V_j for any producer P_j
    NumVotesCollected=math.floor(ProportionProducersRecieveVote*P) #each producer P_j collected V_j NumVotesCollected votes in mempool during phase 2 (t < Delta t_v1)
    #V_j > V_min (and V^maj > V_threshold)
    V_min = math.floor(NumVotesCollected*0.5)  #that is 50% of collected data, in reality V_min should depends on V_j and NumVotesCollected > V_min
    #L_n(prod) = Ln_prod: the final list of producers made by P_j
    #Identifier of producer P_k is added to Ln_prod if it is incuded in 50%P of lists L_k(prod) verifying h_{Delta k} = h^maj_{Delta j}
    Ln_prod=[]

    #lj_prod_sampled = each producer collects NumVotesCollected = V_j lists lj_prod where each list is made of x < NumDeltasCollected identifiers  and merge to lj_prod_sampled
    #lj_prod_sampled[i] gives a matric of vote collected and each vote the number of delta collected. 
    lj_prod_sampled =numpy.zeros((NumDeltasSame,NumVotesCollected,NumDeltasCollected),int)
    #P2_IDs, each row contains index of which producer's vote have been collected by each producer
    P2_IDs = numpy.zeros((NumDeltasSame,NumVotesCollected),int)
    for i in range(NumDeltasSame):
        P2_IDs[i,:]=random.sample(range(P),NumVotesCollected)
        
    for i in range(NumDeltasSame):
        #for j in range(NumVotesCollected):
            #lj_prod_sampled[i,j,:]= lj_prod[P2_IDs[i,j],:]
        lj_prod_sampled[i,:,:] = [lj_prod[P2_IDs[i,j],:] for j in range(NumVotesCollected)]

    #for i in range(NumDeltasSame):
    #   lj_prod_sampled[i,:,:]= lj_prod[numpy.random.choice(lj_prod.shape[0],NumVotesCollected,replace=False), :]

    #lj_vote1 = each row contains index of producers that P believes to have produced the correct vote, otherwise -1.
    #lj_vote1 may certainly not be a complete representation of the list L_n(vote)
    lj_vote1=numpy.zeros((NumDeltasSame,NumVotesCollected),int)
    for i in range(NumDeltasSame):
        #for each vote check if the number correct delta is greater than K_min
        for k in range(NumVotesCollected):
            if numpy.count_nonzero(IDs_prod[lj_prod_sampled[i,:,k]]==1) > K_min: 
                lj_vote1[i,k] = P_IDs[i,k]
            else:
                lj_vote1[i,k] = - 1
        unique, counts = numpy.unique(lj_prod_sampled[i], return_counts=True)
        correct_producers = dict(zip(unique, counts))
        l_temp = []
        for producer, count in correct_producers.items():
            #Check that producer is a correct producer and appears in more than half of P lists
            if count > P/2 and producer!=-1:
                l_temp.append(producer)
        Ln_prod.append(l_temp)
        
    print("Ln_prod")
    print(Ln_prod)
    print("###############")
    print("Lj_vote")
    print(lj_vote1)
    #Code verifies that Ln_prod = L_prod
    runs = []
    for i in range(NumDeltasSame):
        runs.append(Ln_prod[i]==L_prod)
        #print(i, " ", Ln_prod[i])
    percentage_DeltasSame = numpy.count_nonzero(runs)/NumDeltasSame*100
    print(percentage_DeltasSame,"% identical Ln(prod)")

    #Each producer in NumDeltasSame brodacst lj_vote1. Each producer in P collect ProportionProducersRecieveFinalVote votes
    NumFinalVotesCollected=math.floor(ProportionProducersRecieveFinalVote*P) #each producer P_j collected W_j NumVotesCollected votes in mempool during phase 2 (t < Delta t_v1)
   
    #lj_vote_sampled = each producer collects NumFinalVotesCollected = V_j lists lj_prod where each list is made of x < NumVotesCollected identifiers
    #lj_vote_sampled[i] gives a matric of vote collected and each vote the number of delta collected. 
    lj_vote_sampled =numpy.zeros((P,NumFinalVotesCollected,NumVotesCollected),int)
    for i in range(P):
       lj_vote_sampled[i,:,:]= lj_vote1[numpy.random.choice(lj_vote_sampled.shape[0],NumFinalVotesCollected,replace=False), :]

    Ln_vote=[]
    for i in range(P):
        unique, counts = numpy.unique(lj_vote_sampled[i], return_counts=True)
        correct_producers = dict(zip(unique, counts))
        l_temp = []
        for producer, count in correct_producers.items():
            #Check that producer is a correct producer and appears in more than half of P lists
            if count > P/2 and producer!=-1:
                l_temp.append(producer)
        Ln_vote.append(l_temp)


    runs2 = []
    for i in range(P):
        runs2.append(Ln_vote[i]==L_vote)
        #print(i, " ", Ln_prod[i])
    percentage_VoteSame = numpy.count_nonzero(runs2)/P*100
    print(percentage_VoteSame,"% identical Ln(vote)")

    
P = 10
PropProducersSameDelta = 70 #Actual fraction of producers building the same delta P_n/P
PropOfDeltaCollected = 85 #fraction of delta collected by each producer (same for all) K_j
PropProducersRecieveVote = 85 #fraction of vote collected by each producer (same for all) V_j
no_runs = 10 #for stat (10000 --> 2 digits in percent)
runs = []
for i in range(no_runs):
    runs.append(does_simulated_consensus_produce_correct_ln(P,PropProducersSameDelta*0.01,PropOfDeltaCollected*0.01,PropProducersRecieveVote*0.01,PropProducersRecieveVote*0.01))
    result = numpy.count_nonzero(runs)/no_runs*100
    print(result, "% successful run for params(", P, ", ",PropProducersSameDelta,", ", PropOfDeltaCollected,", ", PropProducersRecieveVote, ")")
