#!/usr/bin/env python
# -*- coding=utf8 -*-

import time
import commands
from multiprocessing import Pool,Process
import os,re
import logger


debug = "debug"
info = "info"
warning = "warning"
critical = "critical"

##重启服务器函数##
def reboot(ip):
    logger.logger.critical("It's to start the %s"%ip)
    (status1, output1) = commands.getstatusoutput('''salt -L %s cmd.run "su - yarn -c 'source .bashrc;jps -lm|grep mapreduce.v2.app.MRAppMaster|grep -v jps|wc -l'"'''%ip)
    if status1:
        print "执行jps命令有误,%s"%ip
        logger.logger.warning("执行jps命令有误,%s"%ip)
        return "执行jps命令有误,%s"%ip
    else:
        if output1.split("\n")[1].strip() == "0":
            (status2, output2) = commands.getstatusoutput("salt -L %s cmd.run 'salt-call hadoop_util.stopnm&&salt-call hadoop_util.stopdn&&init 6'"%ip)
        else:
            print "存在AppMaster,%s"%ip
            logger.logger.critical("存在AppMaster,%s"%ip)
            return "存在AppMaster,%s"%ip
    time.sleep(55)
    while True:
        time.sleep(3)
        (status3, output3) = commands.getstatusoutput("salt -L %s test.ping -t 10"%ip)
        if status3:
            print "执行test.ping有误,%s"%ip
            logger.logger.warning("执行test.ping有误,%s"%ip)
        else:
            logger.logger.warning(output3)
            if output3.count("True") == 1:
                while True:
                    (status4, output4) = commands.getstatusoutput("salt -L %s cmd.run 'salt-call hadoop_util.startdn&&salt-call hadoop_util.startnm'"%ip)
                    if status4:
                        logger.logger.warning("启动hadoop进程有误,%s"%ip)
                    else:
                        time.sleep(5)
                        (status5, output5) = commands.getstatusoutput("salt -L %s cmd.run 'ps -ef|grep datanode|grep -v grep|wc -l'"%ip)
                        if output5.split("\n")[1].strip() == "1":
                            logger.logger.critical("The %s is starting the datanode!"%ip)
                            break
                        else:continue
                break
    return "The %s is starting the datanode!"%ip

##看门狗函数##
def watchdog(host_list):
    #kill掉test.ping的进程
    while True:
        # (status,output) = commands.getstatusoutput("ps -ef|grep 'test.ping'|grep 'bash'|grep -v grep|awk '{print $5}'")
        (status,output) = commands.getstatusoutput("ps -ef|grep -E 'test.ping|hadoop_util'|grep 'salt'|grep -v grep")
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list= reip.findall(output)
        ip_list=list(set(ip_list))
        num = time.strftime('%H:%M',time.localtime(time.time()))
        if len(ip_list) > 0:
            logger.logger.info("%s"%str(ip_list))
            for ip in ip_list:
                if ip in host_list:
                    (status,output) = commands.getstatusoutput("ps -ef|grep %s|grep -v grep|awk -F ' ' '{print $5}'|head -1"%ip)
        if output:
            if int(num.split(":")[0]) - int(output.split(":")[0]) >= 1 or int(num.split(":")[1]) - int(output.split(":")[1]) > 3:
                (status,output) = commands.getstatusoutput("ps -ef|grep 'test.ping'|grep -v grep|awk '{print $2}'")
                for process in output.split("\n"):
                    logger.logger.critical("%s process is --> %s"%(num,process))
                    os.system("kill -9 %s"%process)
        time.sleep(60)
        logger.logger.info("The watchdog process is working !")

##主函数##
def main():
    pool = Pool(1)
    host_list=[]
    ##这里得到需要重启的主机list##
    with open("/tmp/host.txt") as f:
        for line in f:
            host_list.append(line.strip().strip("\n"))

    ##这里启动一个watchdog的进程，主要是salt执行的命令可能会没有返回值##
    process = Process(target=watchdog,args=(host_list,))
    process.start()
    ##这里使用进程池，主要启动reboot函数##
    for ip in host_list:
        time.sleep(5)
        result = pool.apply_async(func=reboot,args=(ip,))

    # watchdog(host_list)
    pool.close()
    pool.join()

    ##当result.successful()为True的时候停止主进程##
    if result.successful():
        logger.logger.critical("All of the servers are rebooted !")
        process.terminate()
    # process.join()

if __name__ == "__main__":
    main()