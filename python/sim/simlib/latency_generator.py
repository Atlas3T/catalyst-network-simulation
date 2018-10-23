import numpy
import scipy.stats

def get_latency_relationships(peers):
    N = len(peers[:,0])
    p = len(peers[0,:])
    M=N*p
    samples = get_latency_rvs(M)

    return numpy.reshape(samples,(N,p))

def get_latency_rvs(M):

    lower = 10
    upper = 300
    mu = 30
    sigma = 10

    return scipy.stats.truncnorm.rvs(
        (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=M)




