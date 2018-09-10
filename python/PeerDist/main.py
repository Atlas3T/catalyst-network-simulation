import time
import matplotlib.pyplot as plt
import Propagation


def main():
    start = time.time()
    N=100000;
    p=10;
    x=2;
    Propagation.savePeerDist(N,p,x)
    #peers = Propagation.loadPeerDist(N,p,2)
    duration = time.time() - start
    print(duration)
    #m = Propagation.disperseMessage(peers,3)

    #plt.hist(m, bins = [0,1,2,3,4,5,6,7,8,9])
    #plt.show()


if __name__ == '__main__':
    main()