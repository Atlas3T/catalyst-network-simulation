import numpy
import scipy.stats

def get_latency_relationships(peers):
    N = len(peers[:,0])
    p = len(peers[0,:])

    lower = 10
    upper = 300
    mu = 30
    sigma = 10

    samples = scipy.stats.truncnorm.rvs(
        (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N*p)

    return numpy.reshape(samples,(N,p))



