#!/usr/bin/env python
# -*- coding=utf8 -*-

"""
获取当前文件名、当前函数名、当前行号
"""
# import sys
# def get_cur_info():
#     print sys._getframe().f_code.co_filename # 当前文件名，可以通过__file__获得
#     print sys._getframe().f_code.co_name # 当前函数名
#     print sys._getframe().f_lineno # 当前行号
# get_cur_info()

"""
You want to write data to a file,but only if it don't already exist on the filesystem.
"""
##On the Python3
# with open("E:/Python/workspace/mycode/test.txt","xt") as f:
#     f.write("hello")

##On the Python2
# import os
# if not os.path.exists("E:/Python/workspace/mycode/test.txt"):
#     with open("E:/Python/workspace/mycode/test.txt","wt") as f:
#         f.write("hello")
# else:
#     print("File is already exits!")


# import urllib2,json
# try:
#     value_dict = {}
#     # url="http://172.16.167.106:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
#     url="http://172.16.172.34:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
#     response = urllib2.urlopen("%s"%(url))
#     result=eval((json.loads(response.read()).get('beans')[0].get('LiveNodes')))
#     for keys in result.keys():
#         if result.get(keys).get("adminState") == "In Service":
#             key = result.get(keys).get("xferaddr").split(":")[0]
#             used = result.get(keys).get("used")
#             capacity = result.get(keys).get("capacity")
#             value_dict[key] = float(used)/float(capacity)
#     with open("/tmp/ip.txt","w") as ip_file:
#         for ip in sorted(value_dict.items(),key=lambda  item:item[1])[:200]:
#             ip_file.write("%s\n"%ip[0])
#         for ip in sorted(value_dict.items(),key=lambda  item:item[1])[-201:-1]:
#             ip_file.write("%s\n"%ip[0])
# except Exception,e:
#     print(str(e))



# import commands,re
#
# reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
# (status,output) = commands.getstatusoutput("su - hadp -c 'hadoop dfsadmin -report'")
# ip_list= reip.findall(output)
# print(ip_list)
# # if int(status) == 0:
# #     for line in output.split("\n"):
# #         if line.count(".") ==

# from datetime import datetime, timedelta
# import commands
#
#
# def delete_applogs():
#     day=str(datetime.now() + timedelta(days=-15)).split(" ")[0]
#     (status,output) = commands.getstatusoutput("""hadoop fs -ls  hdfs://ns10/tmp/app-logs/*/logs| sort -k6,7 -r | awk '{T=$6" "$7}T<"%s 00:00"'|awk '{print $8}'"""%day)
#     with open("/tmp/app-logs.txt","w") as files:
#         if int(status) == 0 and len(output.strip()) > 0:
#             for line in output.split("\n"):
#                 files.write("hdfs dfs -rm -r %s\n"%line)
#         else:
#             pass
#
# if __name__ == "__main__":
#     delete_applogs()


# import os.path
#
# for path in ['/one/two/three','/one/two/three/','/','.','']:
#     print('"%s":"%s"'%(path,os.path.split(path)))

# def avg(first,*rest):
#     return (first + sum(rest)) / (1 + len(rest))
#
# #Simple use
# print (avg(1,2))
# print(avg(1,2,3,4))

# import html
#
# def make_element(name,value,**attrs):
#     keyvals = [' %s*"%s"'%item for item in attrs.items()]
#     attr_str = ''.join(keyvals)
#     element = '<{name}{attrs}>{value}</{name}>'.format(
#         name = name,
#         attrs = attr_str,
#         value = html.escape(value)
#     )
#     return element
#
# # Example
# # Creates '<item size="Large" quantity="6">Albatross</item>'
# ret=make_element('item','Albatross',size='large',quantity=6)
# print(ret)
# # Creates '<p>&;spam&gt;</p>'
# ret=make_element('p','<spam>')
# print(ret)
#
# print("{name} is my friend,and {name} like to play footbal!".format(name = "Jack"))

import urllib2,json
def balancer_ip(num):
    try:
        value_dict = {}
        # url="http://172.16.167.106:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
        # url="http://172.16.172.34:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
        url="http://172.22.90.102:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
        response = urllib2.urlopen("%s"%(url))
        result=eval((json.loads(response.read()).get('beans')[0].get('LiveNodes')))
        for keys in result.keys():
            if result.get(keys).get("adminState") == "In Service":
                key = result.get(keys).get("xferaddr").split(":")[0]
                used = result.get(keys).get("used")
                capacity = result.get(keys).get("capacity")
                value_dict[key] = float(used)/float(capacity)
        # ip_list="172.19.173.44,172.19.173.41,172.19.173.42,172.19.173.38,172.19.173.39,172.19.173.36,172.19.173.37,172.19.173.71,172.19.173.69,172.19.173.65,172.19.173.67,172.19.149.24,172.19.149.23,172.19.149.22,172.19.149.21,172.19.149.20,172.19.149.17,172.19.149.18,172.19.149.15,172.19.149.16,172.19.149.54,172.19.149.53,172.19.149.56,172.19.149.55,172.19.149.58,172.19.161.104,172.19.161.100,172.19.161.108,172.19.149.60,172.19.149.68,172.19.149.62,172.19.149.65,172.19.142.54,172.19.142.80,172.19.142.81,172.19.142.82,172.19.142.83,172.19.142.84,172.19.142.75,172.19.142.76,172.19.142.78,172.16.181.100,172.16.181.108,172.16.181.109,172.16.181.111,172.16.181.112,172.16.181.110,172.16.198.106,172.16.198.101,172.16.176.126,172.16.176.120,172.16.176.122,172.19.164.62,172.19.164.53,172.19.164.52,172.19.164.44,172.19.164.41,172.19.164.48,172.19.164.84,172.19.164.80,172.19.164.79,172.19.164.78,172.19.164.72,172.19.164.96,172.19.164.99,172.19.164.95,172.19.164.94,172.19.162.26,172.19.164.40,172.19.164.30,172.19.164.31,172.19.164.39,172.19.164.12,172.19.164.19,172.19.164.17,172.16.179.50,172.16.179.52,172.16.179.51,172.16.179.47,172.16.179.49,172.19.163.113,172.19.163.132,172.19.163.154,172.19.163.156,172.19.163.150,172.19.164.116,172.19.164.115,172.19.164.114,172.19.164.113,172.19.164.111,172.19.164.103,172.16.186.37,172.16.186.36,172.16.186.35,172.16.186.34,172.16.186.30,172.19.160.154,172.16.186.11,172.16.186.12,172.16.186.13,172.16.186.14,172.16.186.15,172.16.186.16,172.16.186.17,172.16.186.18,172.16.186.22,172.16.186.23,172.16.186.20,172.16.186.21,172.16.186.26,172.16.186.27,172.16.186.25,172.16.186.29,172.19.142.119,172.16.178.80,172.16.178.83,172.16.178.81,172.16.178.82,172.19.150.100,172.16.178.77,172.16.178.75,172.16.178.74,172.16.178.79,172.16.178.78,172.16.178.91,172.16.178.86,172.16.178.85,172.16.178.88,172.16.178.87,172.19.150.122,172.16.178.57,172.19.150.117,172.19.150.115,172.16.178.64,172.16.178.65,172.16.178.40,172.16.178.33,172.16.178.30,172.16.178.37,172.16.178.34,172.16.178.35,172.16.178.41,172.16.178.42,172.16.178.43,172.16.178.15,172.16.178.12,172.16.178.13,172.16.178.18,172.16.178.19,172.16.178.17,172.16.178.23,172.16.178.24,172.16.178.25,172.16.178.26,172.16.178.22,172.16.178.27,172.16.178.28,172.16.178.29,172.19.149.114,172.19.149.116,172.16.178.96,172.19.149.110,172.19.149.112,172.19.149.108,172.16.182.99,172.16.182.97,172.16.182.96,172.16.182.94,172.16.181.15,172.16.181.14,172.16.181.16,172.16.181.17,172.16.182.77,172.16.182.78,172.16.182.75,172.16.182.76,172.16.182.79,172.16.182.73,172.16.182.74,172.16.182.86,172.16.182.87,172.16.182.81,172.16.182.82,172.16.182.83,172.16.182.85,172.16.181.59,172.16.181.57,172.19.150.80,172.19.150.76,172.19.150.40,172.19.150.57,172.19.150.83,172.19.150.86,172.19.150.89,172.19.150.99,172.19.150.29,172.19.150.36,172.19.150.38,172.19.150.17,172.19.161.94"
        ip_list="172.22.84.98,172.22.84.81,172.22.84.73,172.22.84.87,172.22.76.136,172.22.76.166,172.22.76.162,172.22.76.168,172.22.76.154,172.22.95.12,172.22.89.92,172.22.89.56,172.22.89.39,172.22.89.31,172.22.89.22,172.22.92.15,172.22.92.91,172.22.92.85,172.22.92.86,172.22.92.83,172.22.92.34,172.22.90.46,172.22.90.76,172.22.90.50,172.22.90.52,172.22.90.62,172.22.90.63,172.22.90.65,172.22.90.69,172.22.91.26,172.22.91.47,172.22.91.52,172.22.91.59,172.22.91.88,172.22.91.98,172.22.74.31,172.22.74.44,172.22.74.43,172.22.74.28,172.22.74.83,172.22.74.84,172.22.74.52,172.22.74.65,172.22.74.71,172.22.81.69,172.22.81.93,172.22.81.80,172.22.81.35,172.22.81.29,172.22.78.124,172.22.78.122,172.22.78.123,172.22.78.121,172.22.78.120,172.22.78.119,172.22.78.118,172.22.73.131,172.22.73.139,172.22.73.141,172.22.100.52,172.22.100.36,172.22.100.43,172.22.100.45,172.22.100.18,172.22.100.98,172.22.73.129,172.22.75.41,172.22.75.28,172.22.75.20,172.22.75.14,172.22.87.67,172.22.80.47,172.22.79.46,172.22.88.34,172.22.72.27,172.22.72.38,172.22.72.52,172.22.72.54,172.22.72.60,172.22.72.72,172.22.72.74,172.22.72.85,172.22.84.106,172.22.70.74,172.22.84.112,172.22.70.68,172.22.70.64,172.22.70.58,172.22.70.54,172.22.70.41,172.22.70.46,172.22.70.31,172.22.70.35,172.22.70.33,172.22.70.39,172.22.70.37,172.22.70.25,172.22.70.27,172.22.70.21,172.22.70.23"
        for ip in ip_list.split(","):
            print(ip,value_dict.get(ip))
        # with open("/tmp/ip.txt","w") as ip_file:
        #     for ip in sorted(value_dict.items(),key=lambda  item:item[1])[:num]:
        #         ip_file.write("%s\n"%ip[0])
        #     for ip in sorted(value_dict.items(),key=lambda  item:item[1])[-num:]:
        #         ip_file.write("%s\n"%ip[0])
    except Exception,e:
        print(str(e))
        # ret['result']=False
        # ret['details']=str(e)
    else:
        print("True")
        # ret['result']=True
        # ret['details']=""
    # finally:
    #     return ret

if __name__ == "__main__":
    balancer_ip(200)









