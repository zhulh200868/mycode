#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.shortcuts import render,HttpResponse,render_to_response
from django.views.decorators.csrf import csrf_exempt
from salt_api import saltAPI
import models
import time
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
    else:
        jid="1"
        ip="1"
        result="2"
        detail="2"
        t_detail = models.t_exec_jid_detail(jid=jid,ip=ip,result=result,detail=detail)
        t_detail.save()
        print models.t_exec_jid_detail.objects.all()
    return HttpResponse("OK")

@csrf_exempt
def salt_api(request):
    if request.method == "POST":
        sapi = saltAPI()
        client = "local_async"
        fun = str(request.POST.get("fun").strip("u''"))
        tgt = str(request.POST.get("tgt").strip("u''"))
        try:
            arg = str(request.POST.get("arg").strip("u''"))
        except Exception,e:
            arg = ""
        ret = "callback_util"
        expr_form = "list"
        if len(arg) > 0:
            params = {
                    "client":client,
                    "fun":fun,
                    "expr_form":expr_form,
                    "tgt":tgt,
                    "ret":ret,
                    "arg":arg
                }
        else:
            params = {
                    "client":client,
                    "fun":fun,
                    "expr_form":expr_form,
                    "tgt":tgt,
                    "ret":ret,
                }
        result = sapi.saltCmd(params)
        jid = result[0]['jid']
        task_id = time.time()
        no = 1
        ip_num = len(tgt.split(","))
        t_mapping = models.t_exec_mapping(jid=jid,ip_list=tgt,command=fun,no=no,task_id=task_id)
        t_mapping.save()
        t_exec_log = models.t_exec_log(task_id=task_id)
        t_exec_log.save()
    else:
        return HttpResponse(request.GET)
    while True:
        num = models.t_exec_jid_detail.objects.all().filter(jid=jid).count()
        if num == ip_num:
            break
        time.sleep(10)
    return HttpResponse("OK")

def test(request):
    num = models.t_exec_jid_detail.objects.all().filter(jid="20161106185006649626").count()
    print(num)
    return HttpResponse(num)


