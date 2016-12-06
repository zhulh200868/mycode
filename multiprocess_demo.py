#!/usr/bin/env python
# -*- coding=utf8 -*-

from multiprocessing import Pool,Lock
import time


def test(num):
    time.sleep(10)
    print(num)


if __name__ == "__main__":
    lock = Lock()
    lock.acquire()
    lock.release()
    pool = Pool(1)
    for i in range(10):
        pool.apply_async(func=test,args=(i,))
    while True:
        for i in range(100):
            time.sleep(5)
            print "num --> %s"%i
        break
    pool.close()
    pool.join()


