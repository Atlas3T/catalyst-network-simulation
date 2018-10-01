import time
import propagation_time

def main():
    start = time.time()
    N=1000;
    p=10;
    x=10;
    iterations = 100
    
    propagation_time.saveDisperseMessageDist(N,p,x,iterations)
    
    duration = time.time() - start
    print(duration)

if __name__ == '__main__':
    main()
