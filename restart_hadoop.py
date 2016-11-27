#!/usr/bin/env python
# -*- coding=utf8 -*-

import time
import commands
from multiprocessing import Pool,Process
import multiprocessing
import os,re
from logger import logger
import sys
import shutil


# debug = "debug"
# info = "info"
# warning = "warning"
# critical = "critical"

Not_restart_list=[]
Restart_list=[]
class Restarted(object):
    def __init__(self):
        pass
    ##重启nodemanger##
    def restartnm(self,ip):
        logger.info("[%s] It's to start the %s"%(multiprocessing.current_process().name,ip))
        #在这里判断是不是有MRAppMaster
        (status, output) = commands.getstatusoutput('''salt -L %s cmd.run "su - yarn -c 'source .bashrc;jps -lm|grep mapreduce.v2.app.MRAppMaster|grep -v jps|wc -l'"'''%ip)
        if status:
            Not_restart_list.append(ip)
            logger.critical("[%s] [Not_restart_list] The fail ip is --> %s"%(multiprocessing.current_process().name,Not_restart_list))
            logger.critical("[%s] 执行jps命令有误,%s"%(multiprocessing.current_process().name,ip))
            return False
            # return "执行jps命令有误,%s"%ip
        else:
            #判断返回的数据用回车分割后是否是2
            if len(output.split("\n")) == 2 and output.count("Not") == 0:
                if output.split("\n")[1].strip() == "0":
                    for i in range(1,4):
                        (status,output) = commands.getstatusoutput("salt -L %s  hadoop_util.stopnm"%ip)
                        logger.critical("[%s] This is the %s --->%s"%(multiprocessing.current_process().name,i,output))
                        (status,output) = commands.getstatusoutput('''salt -L %s cmd.run "ps -ef|grep yarn|grep -v grep|awk '{print $2}'|xargs kill -9"'''%ip)
                        (status,output) = commands.getstatusoutput("salt -L %s cmd.run 'ps -ef|grep yarn|grep -v grep|wc -l'"%ip)
                        if int(status) == 0:
                            if len(output.split("\n")) == 2 and output.count("Not") == 0:
                                if int(output.split("\n")[1].strip()) == 0:
                                    break
                    time.sleep(2)
                    for i in range(1,4):
                        (status,output) = commands.getstatusoutput("salt -L %s hadoop_util.startnm"%ip)
                        logger.critical("[%s] This is the %s --->%s"%(multiprocessing.current_process().name,i,output))
                        time.sleep(5)
                        (status,output) = commands.getstatusoutput('''salt -L %s cmd.run "ps -ef|grep 'nodemanager.NodeManager'|grep -v grep|wc -l"'''%ip)
                        if int(status) == 0:
                            if len(output.split("\n")) == 2 and output.count("Not") == 0:
                                if int(output.split("\n")[1].strip()) == 1:
                                    Restart_list.append(ip)
                                    logger.critical("[%s]  [Restart_list] The successful number is [ %s ] and the list is  --> %s"%(len(Restart_list),Restart_list))
                                    logger.warning("[%s] The %s is restarted the nodemanager !"%ip)
                                    break
                else:
                    Not_restart_list.append(ip)
                    logger.critical("[%s]  [Not_restart_list] The fail ip is --> %s"%(multiprocessing.current_process().name,Not_restart_list))
                    logger.critical("[%s] 存在AppMaster,%s"%(multiprocessing.current_process().name,ip))
                    return False
                    # return "存在AppMaster,%s"%ip
            else:
                Not_restart_list.append(ip)
                logger.critical("[%s]  [Not_restart_list] The fail ip is --> %s"%(multiprocessing.current_process().name,Not_restart_list))
                logger.critical("[%s] The %s is problem,you must check it!"%(multiprocessing.current_process().name,ip))
                return False
        return True
        # return "The %s is starting the datanode!"%ip
        ##重启nodemanger##
    def restartdn(self,ip):
        logger.info("It's to start the %s"%ip)
        for i in range(3):
            (status,output) = commands.getstatusoutput("salt -L %s  hadoop_util.stopdn"%ip)
            logger.critical(output)
            (status,output) = commands.getstatusoutput('''salt -L %s cmd.run "ps -ef|grep datanode|grep -v grep|awk '{print $2}'|xargs kill -9"'''%ip)
            (status,output) = commands.getstatusoutput("salt -L %s cmd.run 'ps -ef|grep datanode|grep -v grep|wc -l'"%ip)
            if int(status) == 0:
                if len(output.split("\n")) == 2 and output.count("Not") == 0:
                    if int(output.split("\n")[1].strip()) == 0:
                        break
            time.sleep(2)
            for i in range(3):
                (status,output) = commands.getstatusoutput("salt -L %s hadoop_util.startdn"%ip)
                logger.critical(output)
                time.sleep(5)
                (status,output) = commands.getstatusoutput('''salt -L %s cmd.run "ps -ef|grep 'datanode'|grep -v grep|wc -l"'''%ip)
                if int(status) == 0:
                    if len(output.split("\n")) == 2 and output.count("Not") == 0:
                        if int(output.split("\n")[1].strip()) == 1:
                            logger.warning("The %s is restarted the datanode !"%ip)
                            break
            else:
                logger.critical("The %s is problem,you must check it!"%ip)
                return False
        return True
        # return "The %s is starting the datanode!"%ip

##看门狗函数##
def watchdog(host_list):
    #kill掉test.ping的进程
    while True:
        # (status,output) = commands.getstatusoutput("ps -ef|grep 'test.ping'|grep 'bash'|grep -v grep|awk '{print $5}'")
        true_ip=0
        (status,output) = commands.getstatusoutput("ps -ef|grep -E 'test.ping|cmd.run|hadoop_util'|grep 'salt'|grep -v grep")
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list= reip.findall(output)
        ip_list=list(set(ip_list))
        num = time.strftime('%H:%M',time.localtime(time.time()))
        if len(ip_list) > 0:
            logger.info("%s"%str(ip_list))
            for ip in ip_list:
                if ip in host_list:
                    true_ip = ip
                    (status,output) = commands.getstatusoutput("ps -ef|grep %s|grep -v grep|awk -F ' ' '{print $5}'|head -1"%ip)
        if output:
            if int(num.split(":")[0]) - int(output.split(":")[0]) >= 1 or int(num.split(":")[1]) - int(output.split(":")[1]) > 3:
                # (status,output) = commands.getstatusoutput("ps -ef|grep -E 'test.ping|cmd.run|hadoop_util'|grep -v grep|awk '{print $2}'")
                (status,output) = commands.getstatusoutput("ps -ef|grep %s|grep -v grep|awk '{print $2}'"%true_ip)
                for process in output.split("\n"):
                    logger.critical("[%s] %s process is --> %s"%(multiprocessing.current_process().name,num,process))
                    os.system("kill -9 %s"%process)
                logger.critical("[%s] These process are killed ---> %s"%(multiprocessing.current_process().name,output))
        time.sleep(60)
        logger.info("[%s] The watchdog process is working !"%multiprocessing.current_process().name)

def wrap(ip):
    action = sys.argv[1]
    restarted = Restarted()
    # if hasattr(restarted,action):
    func = getattr(restarted,action)
    func(ip)


##主函数##
def main():
    Not_restart_list=[]
    Restart_list=[]
    if len(sys.argv) != 2:
        logger.info("Please input the function name!")
        exit()
    action = sys.argv[1]
    restarted = Restarted()
    if hasattr(restarted,action) is False:
        logger.info("You input the function is wrong!")
        exit()
    pool = Pool(1)
    host_list=[]
    old_host_list=[]
    ##这里得到需要重启的主机list##
    if os.path.exists("/tmp/host.txt"):
        with open("/tmp/host.txt","r") as f:
            for line in f:
                host_list.append(line.strip().strip("\n"))
        if os.path.exists("/tmp/hosts.txt"):
            with open("/tmp/hosts.txt","r") as f:
                for line in f:
                    old_host_list.append(line.strip().strip("\n"))
            host_list.sort()
            old_host_list.sort()
            if host_list == old_host_list:
                logger.info("The host.txt is not changed !")
                exit()
    else:
        logger.info("There is no host.txt!")
        exit()
    ##这里启动一个watchdog的进程，主要是salt执行的命令可能会没有返回值##
    process = Process(target=watchdog,args=(host_list,))
    process.start()
    ##这里使用进程池，主要启动reboot函数##
    for ip in host_list:
        # time.sleep(5)
        result = pool.apply_async(func=wrap,args=(ip,))
        # result = pool.apply_async(func=restartnm,args=(ip,))

    # watchdog(host_list)
    pool.close()
    pool.join()

    ##当result.successful()为True的时候停止主进程##
    if result.successful():
        # logger.critical("These ips are not restart --> %s"%str(Not_restart_list))
        # logger.critical("These ips are successfully restarted --> %s"%str(Restart_list))
        logger.critical("All of the servers are rebooted !")
        shutil.copy("/tmp/host.txt","/tmp/hosts.txt")
        process.terminate()
    # process.join()

if __name__ == "__main__":
    main()