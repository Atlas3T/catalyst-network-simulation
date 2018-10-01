import multiprocessing as mp

NCORE = 8

def process(q, iolock):
    from time import sleep
    while True:
        stuff = q.get()
        if stuff is None:
            break
        print("processing no lock", stuff)
        with iolock:
            print("processing again with lock", stuff)
        sleep(stuff)

if __name__ == '__main__':
    q = mp.Queue(maxsize=NCORE)
    iolock = mp.Lock()
    pool = mp.Pool(NCORE, initializer=process, initargs=(q, iolock))
    for stuff in range(20):
        q.put(stuff)  # blocks until q below its max size
        with iolock:
            print("queued", stuff)
    for _ in range(NCORE):  # tell workers we're done
        q.put(None)
    pool.close()
    pool.join()