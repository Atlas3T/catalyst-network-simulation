import peer_dist

def main():
    N = 1000000
    p = 10
    i = 10
    for x in range(i):
        pr = peer_dist.loadPeerDist(N,p,x)
        print(pr[N-1,:])
        #if not peer_dist.isValid(N,p,pr):
            #print("invalid")
        

if __name__ == '__main__':
    main()
