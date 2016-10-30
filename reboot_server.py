#!/usr/bin/env python
# -*- coding=utf8 -*-

import time
import commands
from multiprocessing import Pool
import os


flag=""

def reboot(ip):
    with open("/tmp/reboot.log","a") as files:
        (status1, output1) = commands.getstatusoutput('''salt -L %s cmd.run "su - yarn -c yarn 'jps -lm|grep mapreduce.v2.app.MRAppMaster|grep -v jps|wc -l'"'''%ip)
        if status1:
            print "执行jps命令有误,%s"%ip
            files.write("执行jps命令有误,%s\n"%ip)
            files.flush()
            return "hello1"
        else:
            if output1.split("\n")[1].strip() == "0":
                (status2, output2) = commands.getstatusoutput("salt -L %s cmd.run 'salt-call hadoop_util.stopnm&&salt-call hadoop_util.stopdn&&init 6'"%ip)
            else:
                print "存在AppMaster,%s"%ip
                files.write("存在AppMaster,%s\n"%ip)
                files.flush()
                return "hello2"
        time.sleep(55)
        while True:
            time.sleep(3)
            (status3, output3) = commands.getstatusoutput("salt -L %s test.ping -t 10"%ip)
            if status3:
                print "执行test.ping有误,%s"%ip
            else:
                print output3
                files.write("%s %s\n"%(time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),output3))
                files.flush()
                if output3.count("True") == 1:
                    while True:
                        (status4, output4) = commands.getstatusoutput("salt -L %s cmd.run 'salt-call hadoop_util.startdn&&salt-call hadoop_util.startnm'"%ip)
                        if status4:
                            print "启动hadoop进程有误,%s"%ip
                        else:
                            time.sleep(5)
                            (status5, output5) = commands.getstatusoutput("salt -L %s cmd.run 'ps -ef|grep datanode|grep -v grep|wc -l'"%ip)
                            if output5.split("\n")[1].strip() == "1":
                                print "0,%s"%ip
                                files.write("%s 0,%s\n"%(time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),ip))
                                files.flush()
                                break
                            else:continue
                    break
        return "hello3"


if __name__ == "__main__":
    pool = Pool(1)
    host_list=[]
    with open("/tmp/host.txt") as f:
        for line in f:
            host_list.append(line.strip().strip("\n"))
    for ip in host_list:
        flag = ip
        pool.apply_async(func=reboot,args=(ip,))

    #kill掉test.ping的进程
    while True:
        if flag == host_list[-1]:
            break
        (status,output) = commands.getstatusoutput("ps -ef|grep 'test.ping'|grep 'bash'|grep -v grep|awk '{print $5}'")
        num = time.strftime('%H:%M',time.localtime(time.time()))
        with open("/tmp/monitor.log","a") as files:
            if output:
                #print output
                if int(num.split(":")[0]) - int(output.split(":")[0]) >= 1 or int(num.split(":")[1]) - int(output.split(":")[1]) > 3:
                    (status,output) = commands.getstatusoutput("ps -ef|grep 'test.ping'|grep -v grep|awk '{print $2}'")
                    for process in output.split("\n"):
                        print "%s process is --> %s"%(num,process)
                        files.write("%s process is --> %s"%(num,process))
                        os.system("kill -9 %s"%process)
            time.sleep(60)
            files.write("%s\n"%num)
    pool.close()
    pool.join()