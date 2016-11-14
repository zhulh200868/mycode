# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import json

url = 'http://127.0.0.1:9099/autodeploy/Savelog/'

def returner(ret):
    with open("/tmp/1.txt","w") as files:
        files.write("%s"%ret)
    ret=json.loads(json.dumps(dealReturnData(ret)))
    for i in range(1,3):
        if(sendRet(ret)):
            break
        else:
            time.sleep(1)

def sendRet(ret):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        if ret['return']['result'] or ret['return']['result'] == "True":
            ret['return']['result'] = "True"
        else:
            ret['return']['result'] = "False"
        data = urllib.urlencode(ret)
        req = urllib2.Request(url, data, headers)
        urllib2.urlopen(req)
        # response = urllib2.urlopen(req)
        # the_page = response.read()
    except Exception, e:
        return False
    return True




def dealReturnData(ret) :
    if 'result' in ret['return'].keys() :
        pass
    else :
        tmpReturn = ret['return']
        isSuccess = True
        comment = ''
        for tmp in tmpReturn.keys() :
            tmpItem = tmpReturn[tmp]
            if tmpItem['result'] == True :
                pass
            else :
                isSuccess = False
            try :
                comment = comment + tmp + ':' + tmpItem['comment'] + ';'
            except KeyError , e:
                comment = comment + tmp + ': ;'
        ret['return'] = {'result':isSuccess,'details':comment}
    return ret
