import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy
import peer_dist
import propagation_hops

def main():
    saveDist(500)
    

def saveDist(N):
    p = 10
    i = 10
    n = 100
    propagation_hops.generate_transaction_hop_distribution(N, p, i, n)

if __name__ == '__main__':
    main()