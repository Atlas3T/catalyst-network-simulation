import numpy
import excel_file_manipulation as ma
import get_lists as gl
import os.path


def run_experiment_hist(spec, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, runs):

    process_id = os.getpid()

    start_producer = spec['num_of_producers']
    start_sce = spec['prop_correct_producers']
    start_prop = spec['prop_collected_quantities']
    for ind_p in range(start_producer, end_producer, step_producer):
        spec['num_of_producers'] = ind_p
        spec['prop_correct_producers'] = start_sce
        while spec['prop_correct_producers'] < end_sce:

            spec['prop_collected_quantities'] = start_prop
            spec['prop_collected_candidates'] = start_prop
            spec['prop_collected_votes'] = start_prop
            while spec['prop_collected_quantities'] < end_prop:
                results = numpy.array([gl.calculate_lists_rate(**spec) for _ in range(runs)])
                outputs = get_result_output(spec['num_of_producers'], spec['prop_correct_producers'], results=results)
                pid = str(os.getpid())
                path_name = "excel/Result_simulation_security_ledger_update" + pid + ".xlsx"
                ma.write_results_to_excel_file(spec, runs=runs, output=outputs, process_id=process_id,
                                               path_name=path_name)  # If this fails we need to retry

                prob_it = numpy.count_nonzero(results[:, 1] > ind_p / 2) / runs
                print(f"P = {ind_p}, "
                      f"prod = {spec['prop_correct_producers']}, "
                      f"update = {spec['prop_collected_quantities']}, "
                      f"vote = {spec['prop_collected_candidates']}, "
                      f"final vote = {spec['prop_collected_votes']} --> {prob_it}")

                spec['prop_collected_quantities'] *= 100
                spec['prop_collected_quantities'] += step_prop * 100
                spec['prop_collected_quantities'] /= 100
                spec['prop_collected_candidates'] = spec['prop_collected_quantities']
                spec['prop_collected_votes'] = spec['prop_collected_quantities']

            spec['prop_correct_producers'] *= 100
            spec['prop_correct_producers'] += step_sce * 100
            spec['prop_correct_producers'] /= 100
            spec['prop_correct_producers'] = int(spec['prop_correct_producers'] * 10000) / 10000


def get_result_output(num_of_producers, prop_correct_producers, results):
    avg_prod = numpy.sum(results[:, 0])
    avg_vote = numpy.sum(results[:, 1])
    num_list100_prod = (numpy.count_nonzero(results[:, 0] == (prop_correct_producers * num_of_producers)))
    num_list100_vote = (numpy.count_nonzero(results[:, 1] == (prop_correct_producers * num_of_producers)))
    num_pass = numpy.count_nonzero(results[:, 1] > num_of_producers / 2)
    num_equal_cn = numpy.count_nonzero(results[:, 1] == (prop_correct_producers * num_of_producers))

    return {
        'avg_prod': avg_prod,
        'avg_vote': avg_vote,
        'num_list100_prod': num_list100_prod,
        'num_list100_vote': num_list100_vote,
        'num_pass': num_pass,
        'num_equal_Cn': num_equal_cn
    }


def print_result_output(num_of_producers, prop_correct_producers, prop_collected_quantities, prop_collected_candidates,
                        prop_collected_votes, runs, output):
    print(f'Parameters: P = {num_of_producers} ({runs} runs)')
    print(f'PropCorrectProducer = {prop_correct_producers * 100}%')
    print(f'PropCollectedUpdate = {prop_collected_quantities * 100}%')
    print(f'PropCollectedCandidate = {prop_collected_candidates * 100}%')
    print(f'PropCollectedVote = {prop_collected_votes * 100}%')
    print('############################')
    print('Averages:')
    print(f'{output["avg_prod"] * 100:10.3f} % producers issue correct Ln(prod)')
    print(f'{output["avg_vote"] * 100:10.3f} % producers issue correct Ln(vote)')
    print('Successful runs:')
    print(f'{output["num_list100_prod"] * 100:10.3f} % runs with no missing data for Ln(prod)')
    print(f'{output["num_list100_vote"] * 100:10.3f} % runs with no missing data for Ln(vote)')
    print('Summary:')
    print(f'{output["num_pass"] * 100:10.3f} % successful runs ( > 50% producers broadcast same update)')
    print('############################')
