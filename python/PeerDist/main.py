import time
import matplotlib.pyplot as plt
import Propagation


def main():
    start = time.time()
    N=1000000;
    p=10;
    x=10;
    Propagation.savePeerDist(N,p,x)


        Propagation.saveDisperseMessageDist(100,p,x,100)
        Propagation.saveDisperseMessageDist(1000, p, x, 100)
        Propagation.saveDisperseMessageDist(10000, p, x, 100)
        Propagation.saveDisperseMessageDist(100000, p, x, 100)

    Propagation.saveDisperseMessageDist(1000000, p, 2, 100)

    a = Propagation.loadDisperseMessageDist(100,p,x, 100)
    b = Propagation.loadDisperseMessageDist(1000, p, x, 100)
    c = Propagation.loadDisperseMessageDist(10000, p, x, 100)
    d = Propagation.loadDisperseMessageDist(100000, p, x, 100)
    e = Propagation.loadDisperseMessageDist(1000000, p, 2, 100)
    plt.plot(a[0, :], a[1, :])
    plt.plot(b[0, :], b[1, :])
    plt.plot(c[0, :], c[1, :])
    plt.plot(d[0, :], d[1, :])
    plt.plot(e[0, :], e[1, :])
    plt.show()
    #duration = time.time() - start
    #print(duration)

if __name__ == '__main__':
    main()