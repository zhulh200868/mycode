#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.shortcuts import render,HttpResponse,render_to_response
from django.views.decorators.csrf import csrf_exempt
from salt_api import saltAPI
import models
import time,sys,os
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/"))
sys.path.append(base_dir)
from logger import logger
# Create your views here.

# http://hustxiaoxian.lofter.com/post/1cc7b162_3a6d738

@csrf_exempt
def return_data(request):
    if request.method == "POST":
        jid = str(request.POST.get("jid").strip("u''"))
        ip = str(request.POST.get("id").strip("u''"))
        result = str(request.POST.get("success").strip("u''"))
        detail = str(request.POST.get("return").strip("u''"))
        models.t_exec_jid_detail.objects.all()
        t_detail = models.t_exec_jid_detail(jid=jid, ip=ip,result=result,detail=detail)
        t_detail.save()
        logger.info(request.POST)
    else:
        pass
    return HttpResponse("OK")

@csrf_exempt
def salt_api(request):
    if request.method == "POST":
        sapi = saltAPI()
        client = "local_async"
        fun = str(request.POST.get("fun").strip("u''"))
        tgt = str(request.POST.get("tgt").strip("u''"))
        ret = "callback_util"
        expr_form = "list"
        params = {
                    "client":client,
                    "fun":fun,
                    "expr_form":expr_form,
                    "tgt":tgt,
                    "ret":ret,
                }
        try:
            args = str(request.POST.get("arg").strip("u''"))
            for num,arg in enumerate(args.split("####")):
                params['arg%s'%str(int(num)+1)] = arg
        except Exception,e:
            pass
        print(params)
        result = sapi.saltCmd(params)
        jid = result[0]['jid']
        task_id = time.time()
        no = 1
        ip_num = len(tgt.split(","))
        t_mapping = models.t_exec_mapping(jid=jid,ip_list=tgt,command=fun,no=no,task_id=task_id)
        t_mapping.save()
        t_exec_log = models.t_exec_log(task_id=task_id)
        t_exec_log.save()
        logger.info(request.POST)
        while True:
            num = models.t_exec_jid_detail.objects.all().filter(jid=jid).count()
            if num == ip_num:
                break
            time.sleep(10)
    else:
        return HttpResponse(request.GET)
    return HttpResponse("OK")

def test(request):
    num = models.t_exec_jid_detail.objects.all().filter(jid="20161106185006649626").count()
    print(num)
    return HttpResponse(num)


