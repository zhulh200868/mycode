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
from django import forms
from thread_pool import ThreadPool
# Create your views here.
from django.conf import settings

# http://hustxiaoxian.lofter.com/post/1cc7b162_3a6d738

pool = ThreadPool(5)

#表单
class SaltForm(forms.Form):
    fun = forms.CharField(label='方法',max_length=100)
    tgt = forms.CharField(label='IP列表',widget=forms.PasswordInput())
    arg = forms.CharField(label='参数',widget=forms.PasswordInput())


@csrf_exempt
def return_data(request):
    if request.method == "POST":
        # jid = str(request.POST.get("jid").strip("u''"))
        # ip = str(request.POST.get("id").strip("u''"))
        # result = str(request.POST.get("return")['result'].strip("u''"))
        # detail = str(request.POST.get("return")['details'].strip("u''"))
        jid = request.POST.get("jid").encode()
        ip = request.POST.get("id").encode()
        result=eval(request.POST.get("return").encode())['result']
        detail=eval(request.POST.get("return").encode())['details']
        # models.t_exec_jid_detail.objects.all()
        t_detail = models.t_exec_jid_detail(jid=jid, ip=ip,result=result,detail=detail)
        t_detail.save()
        logger.info(request.POST)
    else:
        pass
    return HttpResponse("OK")

@csrf_exempt
def salt_api(request):
    print(request.POST)
    if request.method == "POST":
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if ip not in settings.CLIENT_SAFE_IF:
            return HttpResponse("The ip is not safe !")
        form_value = SaltForm(request.POST)
        if form_value.is_valid():
            sapi = saltAPI()
            client = "local_async"
            # fun = str(request.POST.get("fun").strip("u''"))
            # tgt = str(request.POST.get("tgt").strip("u''"))
            fun = form_value.cleaned_data['fun']
            tgt = form_value.cleaned_data['tgt']
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
            # args = str(request.POST.get("arg").strip("u''"))
            args = form_value.cleaned_data['arg']
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
        counter = 0
        flag = ""
        total_ip_list=[]
        success_ip_list=[]
        fail_ip_list=[]
        while True:
            T_num = models.t_exec_jid_detail.objects.all().filter(jid=jid,result='True').count()
            F_num = models.t_exec_jid_detail.objects.all().filter(jid=jid,result='False').count()
            if (int(T_num) + int(F_num)) == ip_num:
                if int(T_num) == ip_num:
                    flag = True
                else:
                    flag = False
                break

            else:
                if counter == 30:
                    flag = False
                    break
                else:
                    counter += 1
                    time.sleep(10)
        if flag:
            for i in tgt:
                success_ip_list.append(i)
            return HttpResponse("The command is successful !%s"%success_ip_list)
        else:
            ip_list = models.t_exec_jid_detail.objects.all().values('ip').filter(jid=jid,result='False')
            for i in ip_list:
                fail_ip_list.append(i['ip'])
            ip_list = models.t_exec_jid_detail.objects.all().values('ip').filter(jid=jid,result='True')
            for i in ip_list:
                success_ip_list.append(i['ip'])
            return HttpResponse("Wait 5 minutes,there is not all minion! fail_list:%s,success_list:%s"%(fail_ip_list,success_ip_list))
    else:
        return HttpResponse(request.GET)

def test(request):
    pass



