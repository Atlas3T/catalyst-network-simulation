import numpy
import scipy
import propagation_time

def getProfileSetTimePath(time ,p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/profile_set_time_' + str(time)+ '_' + str(p) + "_" + str(x)+ "_" + str(i))

def getProfileSetPercentPath(percent, p, x, i):
    return os.path.normpath(getFilePathRoot() + '/prob_dist_time/profile_set_percent_' + str(percent) + '_' + str(p) + "_" + str(x)+ "_" + str(i))


def percentage_under_cuttoff_latency(listofN,p,x,iterations,ms):
    list = []
    for N in listofN:
        dist = propagation_time.load_transaction_time_distribution(N,p,x,iterations)
        d = dist.flatten()
        no_under = numpy.count_nonzero(d < ms)
        result = no_under/len(d)
        list.append ([N,result])
    fileName = getProfileSetTimePath(ms,p,x,iterations)
    scipy.io.savemat(fileName, {"profile": list}, appendmat=True)
    print(list)

def latency_at_cuttoff_percentage(listofN,p,x,iterations,percentage):
    list=[]
    for N in listofN:
        dist = propagation_time.load_transaction_time_distribution(N,p,x,iterations)
        d = dist.flatten()
        result = numpy.percentile(d,percentage)
        list.append([N,result])
    fileName = getProfileSetPercentPath(percentage,p,x,iterations)
    scipy.io.savemat(fileName, {"profile": list}, appendmat=True)
    print(list)

def load_p_u_c_l(ms,p,x,iterations):
    fileName = getProfileSetTimePath(ms,p,x,iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    list = contents['profile']
    return list.tolist()

def load_l_a_c_p(percentage,p,x,iterations):
    fileName = getProfileSetPercentPath(percentage,p,x,iterations)
    contents = scipy.io.loadmat(fileName,  appendmat=True)
    list = contents['profile']
    return list.tolist()