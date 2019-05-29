import numpy
import random
import math
import argparse
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
        ratio_threshold = 0.5 + 4 * math.sqrt(ratio_maj * (1 - ratio_maj) / num_collected_data)
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
        if lists_to_compare[i] == correct_list:
            count_list_complete.append(i)
    return count_list_complete


def calculate_lists_rate(num_of_producers, prop_correct_producers, prop_collected_update, prop_collected_vote,
                         prop_collected_final_vote):
    """
    This function checks how many producers manage to compile the correct lists Ln(prod) and Ln(vote)
    :param num_of_producers: Number of producers (P)
    :param prop_correct_producers: Fraction of producers who correctly build the dominant ledger state update (K_n/P)
    :param prop_collected_update: Fraction of collected ledger state update per producer (K_j/P)
    :param prop_collected_vote: Fraction of collected vote per producer (V_j/P)
    :param prop_collected_final_vote: Fraction of collected final vote per producer (W_j/P)
    :return: result (int, int) where the first is the fraction of producers among K_n having correctly built Ln(prod)
    and the second is the fraction of producers among P having correctly built Ln(vote)
    """
    result = numpy.zeros(2, int)

    # Range to experiment [0.55,0.99]
    num_of_correct_updates = math.floor(prop_correct_producers * num_of_producers)

    # Producers flag: 1 if associated to correct update, 0 otherwise
    correct_update_flags = numpy.zeros(num_of_producers, int)
    correct_update_flags[:num_of_correct_updates] = 1

    # True list of correct producers (K_n)
    correct_update_ids = [i for i in range(num_of_correct_updates)]

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
    num_of_collected_votes = math.floor(prop_collected_vote * num_of_producers)

    # List of producer ids associated to votes collected by producer
    collected_vote_ids = get_list_producer_ids(num_of_producers, num_of_collected_votes)
    collected_vote_ids = collected_vote_ids[0:num_of_correct_updates, :]

    # Set of lj_prod collected by each producer
    lj_prod_sampled = numpy.zeros((num_of_correct_updates, num_of_collected_votes, num_of_collected_updates), int)
    for i in range(num_of_correct_updates):
        lj_prod_sampled[i, :, :] = [lj_prod[collected_vote_ids[i, j], :] for j in range(num_of_collected_votes)]

    # List of producers associated to correct update merged by each producers (compare with correct_update_ids)
    compare_correct_update_ids = get_merged_list_ids(num_of_correct_updates, lj_prod_sampled, num_of_producers/2)

    producer_ids_full_list_prod = get_ids_with_full_lists(num_of_correct_updates, correct_update_ids,
                                                          compare_correct_update_ids)

    # percentage_correct_list_prod = len(producer_ids_full_list_prod)/num_of_producers
    # print("{:10.3f} % identical Ln(prod)".format(percentage_correct_list_prod * 100))

    # List of producer ids associated to correct vote collected by producer, -1 otherwise
    lj_vote = numpy.zeros((num_of_correct_updates, num_of_collected_votes), int)
    for i in range(num_of_correct_updates):
        majority_i = get_list_producers_who_found_majority(num_of_collected_votes, correct_update_flags,
                                                           lj_prod_sampled[i, :, :], num_of_collected_votes)

        lj_vote[i, :] = [collected_vote_ids[i, k] if majority_i[k] == 1 and k in producer_ids_full_list_prod else -1
                         for k in range(num_of_collected_votes)]

    # W_j <=  num_of_correct_updates final votes collected per producer. Range to experiment [0.75,0.99]
    num_of_collected_final_votes = math.floor(prop_collected_final_vote * num_of_correct_updates)

    # Set of lj_vote collected by each producer
    lj_vote_sampled = numpy.zeros((num_of_producers, num_of_collected_final_votes, num_of_collected_votes), int)
    threshold_vote_list = len(correct_update_ids) / 2

    for i in range(num_of_producers):
        lj_vote_sampled[i, :, :] = lj_vote[numpy.random.choice(lj_vote.shape[0], num_of_collected_final_votes,
                                                               replace=False), :]
        if numpy.count_nonzero(lj_vote_sampled[i, :] != -1) < threshold_vote_list:
            lj_vote_sampled[i, :, :] = -1

    compare_correct_vote_producer_ids = get_merged_list_ids(num_of_producers, lj_vote_sampled, threshold_vote_list)

    producer_ids_full_list_vote = get_ids_with_full_lists(num_of_producers, correct_vote_ids,
                                                          compare_correct_vote_producer_ids)

    # percentage_correct_list_vote = len(producer_ids_full_list_vote)/num_of_producers
    # print("{:10.3f} % identical Ln(vote)".format(percentage_correct_list_vote * 100))

    result = [len(producer_ids_full_list_prod), len(producer_ids_full_list_vote)]

    return result


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--p', type=int, default=200, help='Number of producers')
    parser.add_argument('--runs', type=int, default=50, help='Number of runs')
    parser.add_argument('--producer', type=float, default=0.8, help='Proportion of correct producers')
    parser.add_argument('--update', type=float, default=0.8, help='Proportion of collected updates per producer')
    parser.add_argument('--vote', type=float, default=0.8, help='Proportion of collected votes per producer')
    parser.add_argument('--final', type=float, default=0.8, help='Proportion of collected final votes')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    res = numpy.array([calculate_lists_rate(args.p, args.producer, args.update, args.vote, args.final)
                       for _ in range(args.runs)])

    print("Parameters: P = {}. {} runs \n propCorrectProducer = {} \n propCollectedUpdate = {} \n propCollectedVote "
          "= {} \n propCollectedFinalVote = {}\n ".format(args.p, args.runs, args.producer, args.update, args.vote,
                                                          args.final))
    print("############################")
    print("Averages:")
    print("{:10.3f} % producers issue correct Ln(prod)".format(numpy.mean(res[:, 0]) / args.p * 100))
    print("{:10.3f} % producers issue correct Ln(vote)".format(numpy.mean(res[:, 1]) / args.p * 100))
    print("############################")
    print("Successful runs:")
    print("{:10.3f} % runs with no missing data for Ln(prod)".format((1-numpy.count_nonzero(res[:, 0] - args.producer *
                                                                                            args.p) / args.runs) * 100))
    print("{:10.3f} % runs with no missing data for Ln(vote)".format((1-numpy.count_nonzero(res[:, 1] - args.p) /
                                                                      args.runs) * 100))
    print("############################")
    print("{:10.3f} % successful runs ( > 50% producers broadcast same update)".format(numpy.count_nonzero(
        res[:, 1] > args.p/2) / args.runs * 100))
