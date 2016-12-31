#!/usr/bin/env python
# -*- coding=utf8 -*-

'''
方法一：
'''
# import urllib
# import urllib2
# url = "http://bdpops.jd.com/autodeploy/ipManage/list.html"
# req = urllib2.Request(url)
# print(req)
#
# res_data = urllib2.urlopen(req)
# res = res_data.read()
# print(res)

'''
方法二：
'''

import httplib

url = "http://bdpops.jd.com/autodeploy/ipManage/list.html"
conn = httplib.HTTPConnection("172.22.91.79")
conn.request(method="GET",url=url)
response = conn.getresponse()
res = response.read()
print(res)