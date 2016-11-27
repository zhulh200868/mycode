#!/usr/bin/env python
# -*- coding=utf8 -*-


import urllib2
import urllib
import os
import time
import hashlib


url='http://zeus.jd.com:8888/api'
#url='http://172.22.99.105:8888/api'
file_name = "E:\Python\workspace\mycode\Aircraftcarrier\Ronaldo\dns_ip.txt"
meg={}

def check_dns_ip_file(func):
    def wrapper():
        try:
            if os.path.exists(file_name) is not True:
                exit("%s文件不存在！"%file_name)
            with open(file_name,"r") as f:
                for val in f:
                    if len(val.strip("\n").split(",")) == 2 or len(val.strip("\n").split(",")) == 3:
                        continue
                    elif val.startswith('#') or len(val.strip("\n").split(",")) == 1:
                            continue
                    else:exit("%s文件格式不对！"%file_name)
            return func()
        except Exception,e:
            print(e)
    return wrapper



@check_dns_ip_file
def create_meg():
    with open(file_name,"r") as f:
        temp=[]
        for index,val in enumerate(f):
            if val.startswith('#') or len(val.strip("\n").split(",")) == 1:
                continue
            # meg = {'tag':'011','token':'','proline':'','cluster':'','ips':[]}
            meg = {'tag':'010','ips':'','user':'zhulinhai','isClient':'','cluster':'','token':''}
            value = val.strip("\n").split(",")
            meg['ips'] = value[0].strip()
            if len(value) == 2:
                meg['isClient'] = '1'
                meg['cluster'] = 'druid'
            else:
                meg['isClient'] = '0'
                meg['cluster'] = value[2].strip()
            temp.append(value[0])
        str = ",".join(temp)
        meg['ips'] = str
        user = 'zhulinhai'
        daytime = time.strftime('%Y%m%d',time.localtime())
        tk = daytime + user
        token = hashlib.md5(tk).hexdigest()
        meg['token'] = token
    return meg

def post_meg(data):
    # data={'user':'zhulinhai','token':'%s'%data['token'],'tag':'011','proline':'hadoop','cluster':'druid','ips':'%s'%data['ips'],'isClient':0}
    #data={'user':'zhulinhai','tag':'010','hostname':'%s'%data['hostname'],'ips':'%s'%data['ipaddr'],'isClient':0}
    data={'user':'zhulinhai','tag':'010','cluster':'%s'%data['cluster'],'ips':'%s'%data['ips'],'isClient':'%s'%data['isClient'],'token':'%s'%data['token']}
    print data
    data = urllib.urlencode(data)
    req = urllib2.urlopen(url,data)
    #获取提交后返回的信息
    result = req.read()
    return result

def main():
    #try:
    data = create_meg()
    print post_meg(data)
    #     post_data = post_meg(data)
    #     print "执行结果为:-->",post_data
    #     content="本次添加dns的主机如下：\n"
    #     for ip in data["ips"].split(","):
    #         content += "%s\n"%ip
    #     print content
    # except Exception,e:
    #     print e

if __name__ == "__main__":
    main()
