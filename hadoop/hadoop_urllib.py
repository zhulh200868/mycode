#!/usr/bin/env python
# -*- coding=utf8 -*-

import thread_pool
import urllib2
import re
import commands
import threading
import sys

def curl(ip):
    response = urllib2.urlopen("http://%s:%s/conf"%(ip,port))
    for rep in  response.read().split("\n"):
        if rep.count("%s"%arg) == 1:
            p=re.compile(r'(?<=<value>)(.*?)(?=</value>)')
            value = re.findall(p,rep)
            if lock.acquire():
                if len(value) == 1:
                    if value[0] == "%s"%values:
                        with open("/tmp/1.txt","a") as curl_file:
                            curl_file.write("%s %s\n"%(ip,value[0]))
                    else:
                        with open("/tmp/2.txt","a") as curl_file:
                            curl_file.write("%s %s\n"%(ip,value[0]))
                lock.release()

def callback(success, result):
    pass
    # print("id-->%s,success-->%s"%(ip,success))

if __name__ == "__main__":
    """
    python hadoop_urllib.py 'yarn.nodemanager.resource.percentage-physical-cpu-limit' '90' 8042
    """
    arg = sys.argv[1]
    values = sys.argv[2]
    port = sys.argv[3]
    lock = threading.Lock()
    pool = thread_pool.ThreadPool(10)
   # (status,ip_list) = commands.getstatusoutput("python /root/yangsong/getIP.py basketball hadoop-dn")
    status=0
    ip_list="172.16.160.111,172.19.143.132,172.19.143.135,172.19.149.77,172.19.149.94,172.19.149.85,172.16.159.21,172.16.159.41,172.19.142.82,172.19.142.83,172.19.142.79,172.19.142.95,172.16.165.114,172.16.165.141,172.16.159.98,172.16.159.85,172.19.156.139,172.19.156.107,172.19.156.100,172.16.163.106,172.16.163.116,172.19.159.130,172.19.146.112,172.19.159.155,172.19.143.17,172.19.143.16,172.19.143.28,172.19.143.26,172.19.159.107,172.19.159.115,172.19.162.20,172.19.162.71,172.19.162.70,172.19.163.107,172.19.163.101,172.19.160.26,172.19.160.23,172.19.160.139,172.19.160.143,172.19.146.87,172.19.147.113,172.19.147.114,172.19.147.108,172.19.147.130,172.16.164.34,172.19.147.120,172.19.157.23,172.19.146.18,172.19.157.39,172.16.170.54,172.16.170.66,172.19.148.110,172.19.148.112,172.19.148.121,172.19.156.35,172.19.156.40,172.19.156.69,172.19.161.34,172.19.161.39,172.19.161.42,172.19.158.42,172.19.162.111,172.19.161.26,172.19.162.106,172.19.161.29,172.19.158.23,172.19.158.22,172.19.161.77,172.19.161.73,172.19.161.92,172.19.158.94,172.19.144.138,172.19.162.144,172.19.162.145,172.19.162.149,172.19.158.52,172.19.158.122,172.19.151.78,172.19.151.26,172.19.151.28,172.19.151.22,172.19.144.25,172.19.151.31,172.16.173.27,172.19.152.125,172.19.148.34,172.19.148.31,172.19.148.79,172.19.148.84,172.19.148.82,172.19.147.24,172.19.152.83,172.19.152.85,172.19.147.60,172.19.147.51,172.19.147.56,172.19.147.54,172.19.147.53,172.19.151.116,172.19.151.108"
    with open("/tmp/1.txt","w") as f1:
        pass
    with open("/tmp/2.txt","w") as f2:
        pass
    if int(status) == 0:
        for ip in ip_list.split(","):
            pool.run(target=curl,args=(ip,),callback=callback)
    pool.close()



