# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import json

url = 'http://172.19.152.40:9000/AutoDeploy/SaveLog.do'

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
    data=json.loads(json.dumps(ret))
    req = urllib2.Request(url, json.JSONEncoder().encode(data))
    try:
        urllib2.urlopen(req)
    except Exception, e:
        with open("/tmp/1.txt","a") as files:
            files.write("%s"%e)
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
