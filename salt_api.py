#!/usr/bin/env python
# -*- coding=utf8 -*-

import urllib2, urllib, json, re


# http://www.xiaomastack.com/2014/11/18/salt-api/

class saltAPI:
    def __init__(self):
        self.__url = 'http://172.22.91.77:8088'       #salt-api监控的地址和端口如:'https://192.168.186.134:8888'
        self.__user =  'salt'             #salt-api用户名
        self.__password = 'wocaonima250'          #salt-api用户密码
        self.__token_id = self.salt_login()

    def salt_login(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content['return']

    def saltCmd(self, params):
        obj = urllib.urlencode(params)
        obj, number = re.subn("arg\d", 'arg', obj)
        res = self.postRequest(obj)
        return res

def main():
    #以下是用来测试saltAPI类的部分
    sapi = saltAPI()
    # params = {'client':'local', 'fun':'test.ping', 'tgt':'172.22.91.79'}
    # #params = {'client':'local', 'fun':'test.ping', 'tgt':'某台服务器的key'}
    # #params = {'client':'local', 'fun':'test.echo', 'tgt':'某台服务器的key', 'arg1':'hello'}
    # #params = {'client':'local', 'fun':'test.ping', 'tgt':'某组服务器的组名', 'expr_form':'nodegroup'}

    params = {'client':'local', 'fun':'user_util.download_configure', 'tgt':'172.18.144.121,172.18.144.122','arg1':'decare','arg2':'zhengchenyu','arg3':'zhengchenyu'}
    test = sapi.saltCmd(params)
    print test
    params = {'client':'local', 'fun':'user_util.modify_hadoop_configure', 'tgt':'172.18.144.121,172.18.144.122','arg1':'decare','arg2':'dd_edw','arg3':'zhengchenyu','arg4':'zhengchenyu'}
    test = sapi.saltCmd(params)
    print test

if __name__ == '__main__':
    main()