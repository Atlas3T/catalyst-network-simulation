import excel_file_manipulation as ma
import generate_output_files as sso
import multiprocessing as mp


def run_multiprocessing(spec_test, step_producer, end_producer, step_sce, end_sce, step_prop, end_prop, runs):
    for num in range(num_processes):
        mp.Process(target=sso.run_experiment_hist, args=(spec_test, step_producer, end_producer, step_sce, end_sce,
                                                         step_prop, end_prop, runs)).start()


if __name__ == '__main__':

    num_processes = 2

    spec = {
        'num_of_producers': 200,
        'prop_correct_producers': 0.75,
        'prop_collected_quantities': 0.75,
        'prop_collected_candidates': 0.75,
        'prop_collected_votes': 0.75 #this needs to be determined by the bloom filters 
    }



    step_producer = 100
    end_producer = 201

    step_sce = 0.01
    end_sce = 0.77

    step_prop = 0.01
    end_prop = 0.77

    spec_test = spec.copy()

    runs = 5

    # Removes any old excel files from previous runs of the script
    move_old_files = mp.Process(target=ma.move_old_excel, args=())

    move_old_files.start()
    move_old_files.join()

    print('begin multiple runs')

    run_multiprocessing_runs = mp.Process(target=run_multiprocessing, args=(spec_test, step_producer, end_producer,
                                                                            step_sce, end_sce, step_prop, end_prop,
                                                                            runs))
    run_multiprocessing_runs.start()
    run_multiprocessing_runs.join()

    combine_excel = mp.Process(ma.combine_excel_files(end_producer, step_producer, spec))
    print("Combining excel files")
    combine_excel.start()
    combine_excel.join()