import numpy

def get_latency_relationships(peers):
    N = len(peers[:,0])
    print(N)
    p = len(peers[0,:])
    print(p)

    return numpy.random.normal(0.5,1.5,(N,p))



