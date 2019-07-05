import create_plots
import post_processing

def get_Plot_Data(ms,p,x,iterations):

    ms = 120
    p = 10
    x = 10
    iterations = 100
    y = post_processing.load_p_u_c_l(ms,p,x,iterations)
    print (y) 
    print (ms)

