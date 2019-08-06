import numpy
import excel_file_manipulation as ma
import get_lists as gl
import argparse
import os.path
import multiprocessing as mp


def if_test_pass(ind_p, process_id, results_test, runs_full, runs_test, spec):
    results_full = numpy.array([gl.calculate_lists_rate(**spec) for _ in range(runs_full)])
    
    results = numpy.concatenate((results_test, results_full))
    runs = runs_full + runs_test
    outputs = get_result_output(spec['num_of_producers'],
                                spec['prop_correct_producers'],
                                spec['prop_collected_votes'],
                                runs=runs, results=results)
    pid = str(os.getpid())
    path_name = "excel/Result_simulation_security_ledger_update" + pid + ".xlsx"
    ma.write_results_to_excel_file(spec, runs=runs, output=outputs, process_id=process_id,
                                path_name=path_name) #If this fails we need to retry 
        
    prob_it = numpy.count_nonzero(results[:, 1] > ind_p / 2) / runs
    print(f"P = {ind_p}, "
            f"prod = {spec['prop_correct_producers']}, "  
            f"update = {spec['prop_collected_quantities']}, "
            f"vote = {spec['prop_collected_candidates']}, "
            f"final vote = {spec['prop_collected_votes']} --> {prob_it}")
    return prob_it

def run_experiment_hist(spec, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, runs_test, runs_full):
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
            prob_it = 0
            while spec['prop_collected_quantities'] < end_prop:
                results_test = numpy.array([gl.calculate_lists_rate(**spec) for _ in range(runs_test)])
                test_pass = numpy.count_nonzero(results_test[:, 1] > ind_p / 2) / runs_test
                '''
                print("P = ",ind_p, ", a=", spec['prop_correct_producers'], ", b=",
                        spec['prop_collected_quantities'], ", c=", spec['prop_collected_candidates'],
                        ", d=", spec['prop_collected_votes'], " -->", test_pass, "-->", process_id)
                
                if test_pass >= 0.6:
                ''' 
                prob_it = if_test_pass(ind_p, process_id, results_test, runs_full, runs_test, spec)
                   
                spec['prop_collected_quantities'] *= 100
                spec['prop_collected_quantities'] += step_prop*100
                spec['prop_collected_quantities'] /= 100
                spec['prop_collected_candidates'] = spec['prop_collected_quantities']
                spec['prop_collected_votes'] = spec['prop_collected_quantities']

                '''
                if prob_it > 0.999:
                    spec['prop_collected_quantities'] = end_prop
                    spec['prop_collected_candidates'] = spec['prop_collected_quantities']
                    spec['prop_collected_votes'] = spec['prop_collected_quantities']
                '''
            spec['prop_correct_producers'] *= 100
            spec['prop_correct_producers'] += step_sce*100
            spec['prop_correct_producers'] /= 100
            spec['prop_correct_producers'] = int(spec['prop_correct_producers']*10000)/10000
            
                     
def run_experiment_grad(spec, step_producer, end_producer, step_prop, end_prop, runs_test, runs_full):

    start_producer = spec['num_of_producers']
    start_prop = spec['prop_correct_producers']
    for ind_p in range(start_producer, end_producer, step_producer):
        list_pass_params = numpy.array([[1, 1, 1, 1]])
        spec['num_of_producers'] = ind_p
        spec['prop_correct_producers'] = start_prop
        while spec['prop_correct_producers'] < end_prop:
            spec['prop_collected_quantities'] = start_prop
            while spec['prop_collected_quantities'] < end_prop:
                spec['prop_collected_candidates'] = start_prop
                while spec['prop_collected_candidates'] < end_prop:
                    spec['prop_collected_votes'] = start_prop
                    while spec['prop_collected_votes'] < end_prop:
                        list_temp_a = list_pass_params[
                            (list_pass_params[:, 0] < spec['prop_correct_producers']) &
                            (list_pass_params[:, 1] <= spec['prop_collected_quantities']) &
                            (list_pass_params[:, 2] <= spec['prop_collected_candidates']) &
                            (list_pass_params[:, 3] <= spec['prop_collected_votes'])]

                        list_temp_b = list_pass_params[
                            (list_pass_params[:, 0] == spec['prop_correct_producers']) &
                            (list_pass_params[:, 1] < spec['prop_collected_quantities']) &
                            (list_pass_params[:, 2] <= spec['prop_collected_candidates']) &
                            (list_pass_params[:, 3] <= spec['prop_collected_votes'])]

                        list_temp_c = list_pass_params[
                            (list_pass_params[:, 0] == spec['prop_correct_producers']) &
                            (list_pass_params[:, 1] == spec['prop_collected_quantities']) &
                            (list_pass_params[:, 2] < spec['prop_collected_candidates']) &
                            (list_pass_params[:, 3] <= spec['prop_collected_votes'])]

                        list_temp_d = list_pass_params[
                            (list_pass_params[:, 0] == spec['prop_correct_producers']) &
                            (list_pass_params[:, 1] == spec['prop_collected_quantities']) &
                            (list_pass_params[:, 2] == spec['prop_collected_candidates']) &
                            (list_pass_params[:, 3] < spec['prop_collected_votes'])]

                        if len(list_temp_a) == 0 and len(list_temp_b) == 0 and len(list_temp_c) == 0 \
                                and len(list_temp_d) == 0:
                            results_test = numpy.array([calculate_lists_rate(**spec) for _ in range(runs_test)])
                            test_pass = numpy.count_nonzero(results_test[:, 1] > ind_p / 2) / runs_test

                            print("a=", spec['prop_correct_producers'], ", b=",
                                  spec['prop_collected_quantities'], ", c=", spec['prop_collected_candidates'],
                                  ", d=", spec['prop_collected_votes'], " -->", test_pass)
                            if test_pass > 0.2:
                                results_full = numpy.array([calculate_lists_rate(**spec) for _ in range(runs_full)])

                                results = numpy.concatenate((results_test, results_full))
                                runs = runs_full + runs_test
                                outputs = get_result_output(spec['num_of_producers'],
                                                            spec['prop_correct_producers'],
                                                            runs=runs, results=results)
                                ma.write_results_to_excel_file(spec, runs=runs, output=outputs,
                                                            path_name="Result_simulation_security_bla.xlsx")
                                full_pass = numpy.count_nonzero(results[:, 1] > ind_p / 2) / runs
                                if numpy.count_nonzero(results[:, 1] > ind_p / 2) == runs:
                                    set_params = [[spec['prop_correct_producers'],
                                                  spec['prop_collected_quantities'],
                                                  spec['prop_collected_candidates'],
                                                  spec['prop_collected_votes']]]
                                    list_pass_params = numpy.concatenate((list_pass_params, set_params))
                                    print(list_pass_params)
                                print(f"P = {ind_p}, "
                                      f"prod = {spec['prop_correct_producers']}, "
                                      f"update = {spec['prop_collected_quantities']}, "
                                      f"vote = {spec['prop_collected_candidates']}, "
                                      f"final vote = {spec['prop_collected_votes']} --> {full_pass}")
                                
                        spec['prop_collected_votes'] += step_prop
                        spec['prop_collected_votes'] = int(spec['prop_collected_votes']*10000)/10000
                    spec['prop_collected_candidates'] += step_prop
                    spec['prop_collected_candidates'] = int(spec['prop_collected_candidates']*10000)/10000
                spec['prop_collected_quantities'] += step_prop
                spec['prop_collected_quantities'] = int(spec['prop_collected_quantities']*10000)/10000
            spec['prop_correct_producers'] += step_prop
            spec['prop_correct_producers'] = int(spec['prop_correct_producers']*10000)/10000


# Functions for output results
def get_result_output_old(num_of_producers, prop_correct_producers, runs, results):
    avg_prod = numpy.mean(results[:, 0]) / num_of_producers
    avg_vote = numpy.mean(results[:, 1]) / num_of_producers
    num_list100_prod = (1 - numpy.count_nonzero(results[:, 0] - prop_correct_producers * num_of_producers) / runs)
    num_list100_vote = (1 - numpy.count_nonzero(results[:, 1] - num_of_producers) / runs)
    num_pass = numpy.count_nonzero(results[:, 1] > num_of_producers / 2) / runs

    return {
        'avg_prod': avg_prod,
        'avg_vote': avg_vote,
        'num_list100_prod': num_list100_prod,
        'num_list100_vote': num_list100_vote,
        'num_pass': num_pass
    }

def get_result_output(num_of_producers, prop_correct_producers, prop_collected_votes, runs, results):
    avg_prod = numpy.sum(results[:, 0])
    avg_vote = numpy.sum(results[:, 1])
    num_list100_prod = (numpy.count_nonzero(results[:, 0] == (prop_correct_producers * num_of_producers)))
    num_list100_vote = (numpy.count_nonzero(results[:, 1] == (prop_correct_producers * num_of_producers)))
    num_pass = numpy.count_nonzero(results[:, 1] > num_of_producers / 2) 
    num_equal_Cn = numpy.count_nonzero(results[:, 1] == (prop_correct_producers * num_of_producers)) 

    return {
        'avg_prod': avg_prod,
        'avg_vote': avg_vote,
        'num_list100_prod': num_list100_prod,
        'num_list100_vote': num_list100_vote,
        'num_pass': num_pass,
        'num_equal_Cn': num_equal_Cn
    }


def print_result_output(num_of_producers, prop_correct_producers, prop_collected_quantities, prop_collected_candidates,
                               prop_collected_votes, runs, output):

    print(f'Parameters: P = {num_of_producers} ({runs} runs)')
    print(f'PropCorrectProducer = {prop_correct_producers*100}%')
    print(f'PropCollectedUpdate = {prop_collected_quantities*100}%')
    print(f'PropCollectedCandidate = {prop_collected_candidates*100}%')
    print(f'PropCollectedVote = {prop_collected_votes*100}%')
    print('############################')
    print('Averages:')
    print(f'{output["avg_prod"]*100:10.3f} % producers issue correct Ln(prod)')
    print(f'{output["avg_vote"]*100:10.3f} % producers issue correct Ln(vote)')
    print('Successful runs:')
    print(f'{output["num_list100_prod"]*100:10.3f} % runs with no missing data for Ln(prod)')
    print(f'{output["num_list100_vote"]*100:10.3f} % runs with no missing data for Ln(vote)')
    print('Summary:')
    print(f'{output["num_pass"]*100:10.3f} % successful runs ( > 50% producers broadcast same update)')
    print('############################')


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--p', type=int, default=200, help='Number of producers')
    parser.add_argument('--runs', type=int, default=10, help='Number of runs')
    parser.add_argument('--producer', type=float, default=0.8, help='Proportion of correct producers')
    parser.add_argument('--update', type=float, default=0.8, help='Proportion of collected updates per producer')
    parser.add_argument('--candidate', type=float, default=0.8, help='Proportion of collected candidate per producer')
    parser.add_argument('--vote', type=float, default=0.8, help='Proportion of collected votes')
    return parser.parse_args()


def setup_spec():
    spec = {
        'num_of_producers': 200,
        'prop_correct_producers': 0.75,
        'prop_collected_quantities': 0.75,
        'prop_collected_candidates': 0.75,
        'prop_collected_votes': 0.75
    }
    step_producer = 100
    end_producer = 301
    step_sce = 0.01
    end_sce = 0.81
    step_prop = 0.01
    end_prop = 0.80
    
    spec_test = spec.copy()
    run_test = 10
    run_full = 10
    list_pass_test = []

    return (end_producer, end_prop, end_sce, 
    list_pass_test, run_full, run_test, 
    spec, spec_test, step_producer, 
    step_prop, step_sce)


def run_multiprocessing(spec_test, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, run_test, run_full):
    for num in range(10):
        mp.Process(target=run_experiment_hist, args=(spec_test, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, run_test, run_full)).start()


if __name__ == '__main__':
    
    step_producer = 0
    end_producer = 0
    step_sce = 0
    end_sce = 0
    step_prop = 0
    end_prop = 0
    spec_test = {}
    run_test = 0
    run_full = 0
    list_pass_test = 0
    spec = {}
    
    
    level_test = 4

    
    if level_test == 0:
        print(" No test selected")

    if level_test == 1:
        args = parse_args()
        res = numpy.array([calculate_lists_rate(args.p, args.producer, args.update, 
                                                args.candidate, args.vote)
                           for _ in range(args.runs)])
        output = get_result_output(args.p, args.producer, 
                                   runs=args.runs, results=res)

        print_result_output(args.p, args.producer, 
                                   args.update, args.candidate, 
                                   args.vote, runs=args.runs,
                                   output=output)
    if level_test == 2:
        end_producer, end_prop, end_sce, 
        list_pass_test, run_full, run_test, 
        spec, spec_test, step_producer, 
        step_prop, step_sce = setup_spec()

        run_experiment_grad(spec_test, step_producer, end_producer, step_prop, end_prop, run_test, run_full)

    if level_test == 3: 
        (end_producer, end_prop, end_sce, 
        list_pass_test, run_full, run_test, 
        spec, spec_test, step_producer, 
        step_prop, step_sce) = setup_spec()

        #ma.move_old_excel()

        run_experiment_hist(spec_test, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, run_test, run_full)
        #timestr = mp.get_time()
        os.rename('excel','excel_test') # Saves individual file to its own folder under 'level_3_single_runs'
        os.mkdir('excel')

    if level_test == 4: #This test is the same as above but allows multiprocessing
        (end_producer, end_prop, end_sce, 
        list_pass_test, run_full, run_test, 
        spec, spec_test, step_producer, 
        step_prop, step_sce) = setup_spec()
        
        #Removes any old excel files from previous runs of the script 
        move_old_files = mp.Process(target=ma.move_old_excel,args=())

        move_old_files.start()
        move_old_files.join()

        print('begining multi run')
        
        #Runs the multiprocessing of the run_experiment_hist
        run_multiprocessing_runs = mp.Process(target=run_multiprocessing, args=(spec_test, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, run_test, run_full))
        run_multiprocessing_runs.start()
        run_multiprocessing_runs.join()
        
        combine_excel = mp.Process(ma.combine_excel_files(end_producer, step_producer, spec))    
        print("Combining excel files") 
        combine_excel.start()
        combine_excel.join()