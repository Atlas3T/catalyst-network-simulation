import time
import matplotlib.pyplot as plt
import propagation_time


def main():
    start = time.time()
    N=100;
    p=10;
    x=10;
    
    propagation_time.saveDisperseMessageDist(N,p,x,100)
    
    duration = time.time() - start
    print(duration)

if __name__ == '__main__':
    main()
