import script_security_fast as ssf
import excel_file_manipulation as ma

def create_global_file():
    """
    This function creates a global file

    This takes the old excel files and generates a complete excel file of all values from all runs of the script
    """
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
    
    (end_producer, end_prop, end_sce, 
    list_pass_test, run_full, run_test, 
    spec, spec_test, step_producer, 
    step_prop, step_sce) = ssf.setup_spec()

    ma.move_old_excel()
    ma.combine_global_output_file(end_producer, step_producer, spec)

def create_master_file():
    """
    Generates a processed file from the global file. 
    """
    ma.generate_postprocessed_files()

if __name__ == '__main__':

    create_global_file()
    create_master_file() 

