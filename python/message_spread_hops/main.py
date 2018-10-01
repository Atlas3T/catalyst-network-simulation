import time
import matplotlib.pyplot as plt
import ../PeerDist/Propagation
import numpy
def main():
    start = time.time()
    N=1000000;
    p=10;
    x=10;

    if False:
        Propagation.savePeerDist(N, p, x)

        Propagation.saveDisperseMessageDist(1000000, p, 2, 100)

    a = Propagation.loadDisperseMessageDist(100, p,x, 100)
    b = Propagation.loadDisperseMessageDist(1000, p, x, 100)
    c = Propagation.loadDisperseMessageDist(10000, p, x, 100)
    d = Propagation.loadDisperseMessageDist(100000, p, x, 100)

    #e = Propagation.loadDisperseMessageDist(1000000, p, 2, 100)
    plt.plot(a[0, :], numpy.cumsum(a[1, :]))
    plt.plot(b[0, :], numpy.cumsum(b[1, :]))
    plt.plot(c[0, :], numpy.cumsum(c[1, :]))
    plt.plot(d[0, :], numpy.cumsum(d[1, :]))
    #plt.plot(e[0, :], e[1, :])
    plt.legend(('100 nodes', '1,000 nodes', '10,000 nodes','100,000 nodes'), title = 'Network size')
    plt.xlabel('Path length')
    plt.ylabel('Probability')
    plt.title('Probability distribution of transaction path length')
    plt.savefig('Prob_dist_path_length.png')
    plt.show()

    #duration = time.time() - start
    #print(duration)

if __name__ == '__main__':
    main()