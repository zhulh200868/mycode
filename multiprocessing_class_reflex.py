#!/usr/bin/env python
# -*- coding=utf8 -*-

####多进程调用类的方法，并且使用到反射####

import multiprocessing

class Worker():
    def run(self,msg):
        print("%s,it works!"%msg)

def start_process():
    print("Starting",multiprocessing.current_process().name)

def wrap(meg,func_name):
    worker = Worker()
    func = getattr(worker,func_name)
    func(meg)

if __name__ == "__main__":
    func_name = "run"
    worker = Worker()
    if hasattr(worker,func_name):
        pool = multiprocessing.Pool(processes=2,initializer=start_process,)
        pool.apply_async(func=wrap,args=('Richard',func_name))
        pool.close()
        pool.join()


####以下是运行不成功的错误！####
"""
PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
"""