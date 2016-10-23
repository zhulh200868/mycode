#!/usr/bin/env python
# -*- coding=utf8 -*-

# http://www.cnblogs.com/alex3714/articles/5230609.html
# import time
# from threading import Thread

# class CountdownTask:
#     def __init__(self):
#         self._running = True
#
#     def terminate(self):
#         self._running = False
#
#     def run(self,n):
#         while self._running and n > 0:
#             print('T-minus',n)
#             n -= 1
#             time.sleep(5)
# c = CountdownTask()
# t = Thread(target=c.run,args=(10,))
# t.start()
# c.terminate()
# t.join()

# from threading import Thread,Event
# import time
#
# #Code to execute in an independent thread
# def countdown(n,started_evt):
#     print('countdown starting')
#
#     while n > 0:
#         print('T-minus',n)
#         n -= 1
#         time.sleep(5)
#         if n == 5:
#             started_evt.set()
#
# #Create the event object that will be used to signal startup
# started_evt = Event()
#
# #Launch the thread and pass the startup event
# print('Launching countdown')
# t = Thread(target=countdown,args=(10,started_evt))
# t.start()
#
# #Wait for the thread to start
# started_evt.wait()
# print('countdown is running')


# import threading
# import time
#
# class PeriodicTimer:
#     def __init__(self,interval):
#         self._interval = interval
#         self._flag = 0
#         self._cv = threading.Condition()
#     def start(self):
#         t = threading.Thread(target=self.run)
#         t.daemon = True
#
#         t.start()
#     def run(self):
#         '''
#         Run the timer and notify waiting threads after each interval
#         '''
#         while True:
#             time.sleep(self._interval)
#             with self._cv:
#                 self._flag ^= 1
#                 self._cv.notify_all()
#     def wait_for_tick(self):
#         '''
#         Wait for the next tick of the timer
#         '''
#         with self._cv:
#             last_flag = self._flag
#             while last_flag == self._flag:
#                 self._cv.wait()
#
# # Example use of the timer
# ptimer = PeriodicTimer(5)
# ptimer.start()
#
# # Two threads that synchronize on the timer
# def countdown(nticks):
#     while nticks > 0:
#         ptimer.wait_for_tick()
#         print ('T-minus',nticks)
#         nticks -= 1
#
# def countup(last):
#     n = 0
#     while n < last:
#         ptimer.wait_for_tick()
#         print('Counting',n)
#         n += 1
#
# threading.Thread(target=countdown,args=(10,)).start()
# threading.Thread(target=countup,args=(5,)).start()


# import threading
#
# # Worker thread
# def worker(n,sema):
#     # Wait to be signaled
#     sema.acquire()
#
#     # Do some work
#     print('Working',n)
#
# # Create some threads
# sema = threading.Semaphore(0)
# nworkers = 10
# for n in range(nworkers):
#     t = threading.Thread(target=worker,args=(n,sema,))
#     t.start()
#
#
# sema.release()



#######多线程写文件#######
import time
import threading
import logger

def addNum():
    global num #在每个线程中都获取这个全局变量
    time.sleep(1)
    if lock.acquire(): #修改数据前枷锁
        # with open("E:/1.txt","a") as files:
        num -= 1
        print('num-->%s'%num)
        logger.logger.info('num-->%s'%num)
            # files.write('num-->%s\n'%num)
            # files.flush()
        lock.release() #修改后释放

num = 10  #设定一个共享变量
thread_list = []
lock = threading.Lock() #生成全局锁
for i in range(10):
    t = threading.Thread(target=addNum)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

print('final num:',num)

# import time
# import threading
#
# def addNum():
#     global num #在每个线程中都获取这个全局变量
#     # print('--get num:',num )
#     time.sleep(1)
#     locks.acquire(1) #修改数据前加锁
#     print('num-->%s'%num)
#     num  -= 1 #对此公共变量进行-1操作
#     locks.release() #修改后释放
#
# num = 5  #设定一个共享变量
# thread_list = []
# locks = threading.Lock() #生成全局锁
# for i in range(5):
#     t = threading.Thread(target=addNum)
#     t.start()
#     thread_list.append(t)
#
# for t in thread_list: #等待所有线程执行完毕
#     t.join()
#
# print('final num:', num )

# import threading
# import time
#
# class MyThread(threading.Thread):
#     def run(self):
#         global num
#         time.sleep(1)
#
#         if mutex.acquire(1):
#             num = num+1
#             msg = self.name+' set num to '+str(num)
#             print msg
#             mutex.release()
# num = 0
# mutex = threading.Lock()
# def test():
#     for i in range(5):
#         t = MyThread()
#         t.start()
# if __name__ == '__main__':
#     test()

