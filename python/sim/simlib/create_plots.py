import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy
import os
import propagation_hops
import seaborn as sns
import latency_generator
import propagation_time
import math
from matplotlib.ticker import ScalarFormatter

def main():
    #list = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000,1000000]
    #plot_propagation_hops(list)

    #plot_latency_dist()
    
    plot_profile_set_latency(120)
    
    #plot_latency_set_prob(95)

    #list = [100,1000,10000,100000,1000000]
    #plot_propagation_time(list)






def plot_propagation_hops(listofN):
    p = 10
    i = 10
    n = 100
    lines = []
    plt.figure()
    for (N) in listofN:
        x=propagation_hops.loadDisperseMessageDist(N,p,i,n)
        lines += plt.plot(x[0, :], numpy.cumsum(x[1, :]), label = "{} nodes".format(N))
    labels = [l.get_label() for l in lines]
    plt.legend(lines, labels,title = 'Network size')
    plt.xlabel('Path length (hops between nodes)')
    plt.ylabel('Probability (cummulative)')
    plt.title('Probability distribution of transaction path length')
    plotfolder = os.path.normpath(getPlotsFolder() + '/propagation_dist_hops.pdf')
    plt.savefig(plotfolder)

def plot_propagation_time(listofN):
    p = 10
    i = 10
    n = 100
    lines = []
    plt.figure()
    for N in listofN:
        x=propagation_time.loadDisperseMessageDist(N,p,i,n)
        snsplot = sns.distplot(x, hist_kws={'cumulative': True}, kde_kws={'cumulative': True}, hist=False, label = "{} nodes".format(N))
    plt.xlabel('time (ms)')
    plt.ylabel('Probability (cummulative)')
    plt.title('Probability distribution of transaction arrival time')
    plt.legend(title='Network size')
    plotfolder = os.path.normpath(getPlotsFolder() + '/propagation_dist_time_all' + str(N) + '.pdf')
    snsplot.figure.savefig(plotfolder)

def plot_profile_set_latency(ms):
    p=10
    x=10
    iterations=100
    profile = propagation_time.load_p_u_c_l(ms,p,x,iterations)
    plt.figure()
    newlist = [(elem1, elem2*100) for elem1, elem2 in profile]
    fig, ax1 = plt.subplots()
    ax1.plot(*zip(*newlist), marker = 'o')
    ax1.set_xscale('log')
    ax1.set_xticks([elem1 for elem1, elem2 in profile])
    ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    for label in ax1.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)
    plt.xlabel('Network size')
    plt.ylabel('Percentage')
    plt.ylim(0, 110) 
    plt.title('Percentage of nodes recieving a transaction within {} ms'.format(ms))
    plotfolder = os.path.normpath(getPlotsFolder() + '/profile_latency_' + str(ms) + 'ms.pdf')
    plt.savefig(plotfolder)

    

def plot_latency_set_prob(prob):
    p=10
    x=10
    iterations=100
    profile = propagation_time.load_l_a_c_p(prob,p,x,iterations)
    plt.figure()
    newlist = [(elem2, elem1) for elem1, elem2 in profile]
    fig, ax = plt.subplots()
    plt.plot(*zip(*newlist))
    for axis in [ax.xaxis]:
        axis.set_major_formatter(ScalarFormatter())
    plt.xlabel('network size')
    plt.ylabel('latency (ms)')
    plt.title('Percentage of nodes recieving a transaction within {} percent'.format(prob))
    plotfolder = os.path.normpath(getPlotsFolder() + '/profile_percentage_' + str(prob) + 'ms.pdf')
    plt.savefig(plotfolder)

    

def plot_latency_dist():
    plt.figure()
    latencies = latency_generator.get_latency_rvs(1000000)
    snsplot = sns.distplot(latencies, hist=False)
    plt.xlabel('time (ms)')
    plt.ylabel('Probability')
    plt.title('Probability distribution of latency between nodes')
    plotfolder = os.path.normpath(getPlotsFolder() + '/latency_dist.pdf')
    snsplot.figure.savefig(getPlotsFolder() + '/latency_distribution.pdf')


def getPlotsFolder():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/plots/")

if __name__ == '__main__':
    main()