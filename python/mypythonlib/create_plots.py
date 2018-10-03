import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy
import prob_dist_hops

def main():
    list = [100,1000,10000,100000]
    loadAndPlot(list)

def loadAndPlot_hops(listofN):
    p = 10
    i = 10
    n = 100
    probs=[]
    for (N) in listofN:
        x=prob_dist_hops.loadDisperseMessageDist(N,p,i,n)
        plt.plot(x[0, :], numpy.cumsum(x[1, :]))
    legendtext = [((str(N) + 'nodes') for N in listofN)]
    plt.legend(legendtext, title = 'Network size')
    plt.xlabel('Path length')
    plt.ylabel('Probability')
    plt.title('Probability distribution of transaction path length')
    plt.savefig(getFileRoot() + 'Prob_dist_path_length.png')
    
    pass

    def getFileRoot():
    #return os.path.normpath("C:/Users/fran/PycharmProjects/Distributions/")
    return os.path.normpath("/home/engr/Results/plots/")

if __name__ == '__main__':
    main()