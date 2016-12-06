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
    ip_list=""
    with open("/tmp/1.txt","w") as f1:
        pass
    with open("/tmp/2.txt","w") as f2:
        pass
    if int(status) == 0:
        for ip in ip_list.split(","):
            #print ip
            pool.run(target=curl,args=(ip,),callback=callback)
    pool.close()



