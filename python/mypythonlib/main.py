import time
import matplotlib.pyplot as plt
import peer_dist
import profile

def main():
    peer_dist.run_until_done()

def oldMain():
    start = time.time()
    N=10000000;
    p=10;
    x=1;
    #Propagation.savePeerDist(N,p,x)
    peer_dist.get(N,p,x)
    if False:
        peer_dist.saveDisperseMessageDist(100,p,x,100)
        peer_dist.saveDisperseMessageDist(1000, p, x, 100)
        peer_dist.saveDisperseMessageDist(10000, p, x, 100)
        peer_dist.saveDisperseMessageDist(100000, p, x, 100)

        peer_dist.saveDisperseMessageDist(1000000, p, 2, 100)

        a = peer_dist.loadDisperseMessageDist(100,p,x, 100)
        b = peer_dist.loadDisperseMessageDist(1000, p, x, 100)
        c = peer_dist.loadDisperseMessageDist(10000, p, x, 100)
        d = peer_dist.loadDisperseMessageDist(100000, p, x, 100)
    #e = Propagation.loadDisperseMessageDist(1000000, p, 2, 100)
        plt.plot(a[0, :], a[1, :])
        plt.plot(b[0, :], b[1, :])
        plt.plot(c[0, :], c[1, :])
        plt.plot(d[0, :], d[1, :])
        plt.plot(e[0, :], e[1, :])
        plt.show()
    duration = time.time() - start
    print(duration)

if __name__ == '__main__':
    #profile.run('main()')
    main()
