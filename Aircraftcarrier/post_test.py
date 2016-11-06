#!/usr/bin/env python
# -*- coding=utf8 -*-

import httplib
import urllib
import urllib2
from datetime import *
import time

def sendhttp():
    data = urllib.urlencode({'u_team_id':'125', 'author':'args1', 'body_pic':'[pic]jfjjfj[/pic]','body_text':'nihaoma daye'})
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Accept": "text/plain"}
    print "1111"
    conn = httplib.HTTPConnection('127.0.0.1:9099', timeout=10)
    print "22222"
    conn.request('POST', '/autodeploy/Savelog/', data, headers)
    conn.set_debuglevel(1)
    httpres = conn.getresponse()
    print httpres.status
    print httpres.reason
    #print httpres.read()
def sendurl():
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    url = 'http://127.0.0.1:9099/autodeploy/Savelog/'
    url = 'http://127.0.0.1:9099/autodeploy/salt_api/'
    #url = 'http://www.baidu.com'
    data = {
        'fun':'os_util.useradd',
        'tgt':'172.19.152.40',
        'arg':'zhulh'
    }
    data1 = urllib.urlencode(data)
    # data = urllib.urlencode({'u_team_id':'125', 'author':'args1', 'body_pic':'[pic]jfjjfj[/pic]','body_text':'nihaoma daye'})
    #headers = { 'User-Agent' : user_agent }
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib2.Request(url, data1, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def gethtml():
    request = urllib2.Request('http://192.168.10.37:7080/vdapp/')
    #request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    opener = urllib2.build_opener()
    f= opener.open(request)
    print f.read().decode('utf-8')

if __name__ == '__main__':
    sendurl()