import time
import propagation_time

def main():
    p=10
    x=10
    iterations = 100
    list = [100,500,1000,5000,10000,50000,100000,500000,1000000]
    propagation_time.percentage_under_cuttoff_latency(list,p,x,iterations,200)
    propagation_time.percentage_under_cuttoff_latency(list,p,x,iterations,165)
    propagation_time.percentage_under_cuttoff_latency(list,p,x,iterations,155)
    #propagation_time.latency_at_cuttoff_percentage(list,p,x,iterations,80)



def old_main():
    start = time.time()
    N=1000000
    p=10
    x=10
    iterations = 10
    
    propagation_time.saveDisperseMessageDist(N,p,x,iterations)
    
    duration = time.time() - start
    print(duration)

if __name__ == '__main__':
    main()
