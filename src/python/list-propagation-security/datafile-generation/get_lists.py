import numpy
import math
import random
from itertools import chain


def get_list_producer_ids(num_producers, num_sample):
    list_ids = numpy.zeros((num_producers, num_sample), int)
    for i in range(num_producers):
        list_ids[i, 0] = i
        list_ids[i, 1:num_sample] = random.sample(list(chain(range(0, i), range(i + 1, num_producers))), num_sample - 1)
    return list_ids


def get_list_producers_who_found_majority(num_producer, id_correct_producers, collected_data_ids, num_collected_data):
    majority_found = numpy.zeros(num_producer, int)
    for i in range(num_producer):
        k_maj = numpy.count_nonzero(id_correct_producers[collected_data_ids[i, :]] == 1)
        ratio_maj = k_maj/num_collected_data
        #print(ratio_maj)
        ratio_threshold = 0.5 + 4.22 * math.sqrt(ratio_maj * (1 - ratio_maj) / num_collected_data)
        majority_found[i] = 1 if ratio_maj > ratio_threshold else 0
    return majority_found


def get_partial_list_ids_found(num_producer, id_correct_producers, collected_data_ids, num_collected_data):

    is_majority_found = get_list_producers_who_found_majority(num_producer, id_correct_producers, collected_data_ids,
                                                              num_collected_data)

    partial_list = numpy.zeros((num_producer, num_collected_data), int)
    for i in range(num_producer):
        partial_list[i, :] = -1
        if is_majority_found[i] == 1:
            for j in range(num_collected_data):
                if id_correct_producers[collected_data_ids[i, j]] == 1:
                    partial_list[i, j] = collected_data_ids[i, j]
                else:
                    partial_list[i, j] = -1
    return partial_list


def get_merged_list_ids(num_producer, sampled_lists, merging_threshold):
    merged_list = []
    for i in range(num_producer):
        unique, counts = numpy.unique(sampled_lists[i], return_counts=True)
        correct_producers = dict(zip(unique, counts))
        l_temp = []
        for producer, count in correct_producers.items():
            if count > merging_threshold and producer != -1:
                l_temp.append(producer)
        merged_list.append(l_temp)
    return merged_list


def get_ids_with_full_lists(num_producer, correct_list, lists_to_compare):
    count_list_complete = []
    for i in range(num_producer):
        if numpy.array_equal(lists_to_compare[i],correct_list):
            count_list_complete.append(i)
    return count_list_complete


def calculate_lists_rate(num_of_producers, prop_correct_producers, prop_collected_quantities, prop_collected_candidates,
                         prop_collected_votes):
    """
    This function checks how many producers manage to compile the correct lists Ln(prod) and Ln(vote)
    :param num_of_producers: Number of producers (P)
    :param prop_correct_producers: Fraction of producers who correctly build the dominant ledger state update (C_n/P)
    :param prop_collected_quantities: Fraction of collected ledger state update per producer (C_j/P)
    :param prop_collected_candidates: Fraction of collected candidate per producer (V_j/P)
    :param prop_collected_votes: Fraction of collected vote per producer (U_j/C_n)
    :return: result (int, int) where the first is the fraction of producers among K_n having correctly built Ln(prod)
    and the second is the fraction of producers among P having correctly built Ln(vote)
    """
    result = numpy.zeros(2, int)
    num_of_correct_updates = math.floor(prop_correct_producers * num_of_producers)

    # Producers flag: 1 if associated to correct update, 0 otherwise
    correct_update_flags = numpy.zeros(num_of_producers, int)
    correct_update_flags[:num_of_correct_updates] = 1

    # True list of correct producers (C_n)
    correct_update_ids = numpy.zeros(num_of_producers, int)
    for i in range(num_of_producers):
        correct_update_ids[i] = i if i < num_of_correct_updates else -1

    num_of_collected_quantities = math.floor(prop_collected_quantities * num_of_producers)

    collected_quantities_ids = get_list_producer_ids(num_of_producers, num_of_collected_quantities)

    lj_prod = get_partial_list_ids_found(num_of_producers, correct_update_flags, collected_quantities_ids,
                                         num_of_collected_quantities)

    majority_found_in_quantities_ids = get_list_producers_who_found_majority(num_of_producers, correct_update_flags,
                                                                             collected_quantities_ids,
                                                                             num_of_collected_quantities)

    correct_candidate_flags = numpy.zeros(num_of_producers, int)
    for i in range(num_of_producers):
        correct_candidate_flags[i] = 1 if majority_found_in_quantities_ids[i] == 1 else 0

    correct_vote_ids = numpy.zeros(num_of_producers, int)
    for i in range(num_of_producers):
        correct_vote_ids[i] = i if majority_found_in_quantities_ids[i] == 1 else -1

    num_of_collected_candidates = math.floor(prop_collected_candidates * num_of_producers)

    collected_candidates_ids = get_list_producer_ids(num_of_producers, num_of_collected_candidates)

    ln_prod = numpy.zeros((num_of_producers, num_of_producers), int)

    merging_threshold_prod = num_of_producers*0.5

    for id_producer in range(num_of_correct_updates):
        lj_prod_collected = lj_prod[numpy.random.choice(lj_prod.shape[0], num_of_collected_candidates, replace=False), :]
        unique, counts = numpy.unique(lj_prod_collected, return_counts=True)
        dict_producers = dict(zip(unique, counts))
        ln_prod[id_producer, :] = -1
        for producer, count in dict_producers.items():
            if count > merging_threshold_prod and producer != -1:
                ln_prod[id_producer, producer] = producer

    ids_with_full_list_prod = get_ids_with_full_lists(num_of_correct_updates, correct_update_ids, ln_prod)

    lj_vote = get_partial_list_ids_found(num_of_producers, correct_candidate_flags, collected_candidates_ids,
                                         num_of_collected_candidates)

    num_of_collected_votes = math.floor(prop_collected_votes * num_of_producers)

    ln_vote = numpy.zeros((num_of_correct_updates, num_of_producers), int)

    merging_threshold_vote = num_of_producers * 0.5 #num_of_producers rather than num_of_correct_updates

    # min(num_of_collected_votes, num_of_collected_candidates)
    for id_producer in range(num_of_correct_updates):
        lj_vote_collected = lj_vote[numpy.random.choice(lj_vote.shape[0], num_of_collected_votes, replace=False), :]
        unique, counts = numpy.unique(lj_vote_collected, return_counts=True)
        dict_producers = dict(zip(unique, counts))
        ln_vote[id_producer, :] = -1
        for producer, count in dict_producers.items():
            if count > merging_threshold_vote and producer != -1:
                ln_vote[id_producer, producer] = producer

    ids_with_full_list_vote = get_ids_with_full_lists(num_of_correct_updates, correct_vote_ids, ln_vote)

    result = [len(ids_with_full_list_prod), len(ids_with_full_list_vote)]

    #print("res 1 : ", len(ids_with_full_list_prod))
    #print("res 2 : ", len(ids_with_full_list_vote))
    return result

    '''
    # K_j updates collected per producer. Range to experiment [0.75,0.99], use to determine k_min
    num_of_collected_updates = math.floor(prop_collected_update*num_of_producers)

    # List of producer ids associated to updates collected by producer
    collected_update_ids = get_list_producer_ids(num_of_producers, num_of_collected_updates)

    # List of id of producers who found a dominant update
    majority_found = get_list_producers_who_found_majority(num_of_producers, correct_update_flags, collected_update_ids,
                                                           num_of_collected_updates)

    # List of producer ids associated to correct updates collected by producer, -1 otherwise
    lj_prod = get_partial_list_ids_found(num_of_producers, correct_update_flags, collected_update_ids,
                                         num_of_collected_updates)

    # True list of correct voters
    correct_vote_ids = []
    for i in range(num_of_producers):
        if majority_found[i] == 1:
            correct_vote_ids.append(i)
    correct_vote_ids.sort()

    if len(correct_vote_ids) == 0:
        print("No producer found a majority of same update: abort!")
        return result


    # V_j votes collected per producer. Range to experiment [0.75,0.99]. Use to determine V_min
    num_of_collected_candidate = math.floor(prop_collected_candidate * num_of_producers)



    # List of producer ids associated to votes collected by producer
    collected_vote_ids = get_list_producer_ids(num_of_producers, num_of_collected_candidate)

    collected_vote_ids = collected_vote_ids[0:num_of_correct_updates, :]

    # Set of lj_prod collected by each producer
    lj_prod_sampled = numpy.zeros((num_of_correct_updates, num_of_collected_candidate, num_of_collected_updates), int)
    for i in range(num_of_correct_updates):
        lj_prod_sampled[i, :, :] = [lj_prod[collected_vote_ids[i, j], :] for j in range(num_of_collected_candidate)]

    # List of producers associated to correct update merged by each producers (compare with correct_update_ids)
    compare_correct_update_ids = get_merged_list_ids(num_of_correct_updates, lj_prod_sampled, num_of_producers/2)

    producer_ids_full_list_prod = get_ids_with_full_lists(num_of_correct_updates, correct_update_ids,
                                                          compare_correct_update_ids)

    # List of producer ids associated to correct vote collected by producer, -1 otherwise
    lj_vote = numpy.zeros((num_of_correct_updates, num_of_collected_candidate), int)
    for i in range(num_of_correct_updates):
        majority_i = get_list_producers_who_found_majority(num_of_collected_candidate, correct_update_flags,
                                                           lj_prod_sampled[i, :, :], num_of_collected_updates)

        lj_vote[i, :] = [collected_vote_ids[i, k] if majority_i[k] == 1 and k in producer_ids_full_list_prod else -1
                         for k in range(num_of_collected_candidate)]

    # U_j <=  num_of_correct_updates final votes collected per producer. Range to experiment [0.75,0.99]
    num_of_collected_votes = math.floor(prop_collected_vote * num_of_correct_updates)

    # Set of lj_vote collected by each producer
    lj_vote_sampled = numpy.zeros((num_of_producers, min(num_of_collected_votes, num_of_collected_candidate),
                                   num_of_collected_candidate), int)
    threshold_vote_list = len(correct_update_ids) / 2

    for i in range(num_of_producers):
        lj_vote_sampled[i, :, :] = lj_vote[numpy.random.choice(lj_vote.shape[0], min(num_of_collected_votes,
                                                                                     num_of_collected_candidate),
                                                               replace=False), :]
        if numpy.count_nonzero(lj_vote_sampled[i, :] != -1) < threshold_vote_list:
            lj_vote_sampled[i, :, :] = -1

    compare_correct_vote_producer_ids = get_merged_list_ids(num_of_producers, lj_vote_sampled, threshold_vote_list)

    num_sucessful_prod = int(num_of_producers * prop_correct_producers)

    producer_ids_full_list_vote = get_ids_with_full_lists(num_sucessful_prod, correct_vote_ids,
                                                          compare_correct_vote_producer_ids)

    result = [len(producer_ids_full_list_prod), len(producer_ids_full_list_vote)]
    
    return result
    '''
