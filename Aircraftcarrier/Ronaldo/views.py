#!/usr/bin/env python
# -*- coding=utf8 -*-

from django.shortcuts import render,render_to_response,HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django import forms
from models import User,Command_info
import logger
import urllib
import urllib2
import json
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required

# Create your views here.

#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

#登陆认证https://segmentfault.com/q/1010000007240873
def login_required(func):
    def wrapper(request):
        username = request.COOKIES.get('username','')
        if username:
            return func(request)
        else:
            return render_to_response('login.html')
    return wrapper
#登陆成功
@login_required
def home(request):
    username = request.COOKIES.get('username','')
    logger.logger.info("[username] %s login home !"%username)
    return render_to_response('home.html',{'username':username})
    # return render_to_response('index.html',{'username':username})
    # username = request.COOKIES.get('username','')
    # if username:
    #     logger.logger.info("%s loggin !"%username)
    #     return render_to_response('index.html',{'username':username})
    # else:
    #      return render_to_response('login.html')

@login_required
def autodeploy(request):
    username = request.COOKIES.get('username','')
    logger.logger.info("[username] %s login the autodeploy !"%username)
    cmd_name = Command_info.objects.all().values('cmd_name')
    return render_to_response('autodeploy.html',{'cmd_name':cmd_name,'username':username})



#注册
def regist(request):
    if request.method == 'POST':
        print(request.POST)
        form_value = UserForm(request.POST)
        if form_value.is_valid():
            #获得表单数据
            username = form_value.cleaned_data['username']
            password = form_value.cleaned_data['password']
            User.objects.create(username= username,password=password)
            # first_password = form_value.cleaned_data['first_password']
            # second_password = form_value.cleaned_data['second_password']
            # lname = form_value.cleaned_data['lname']
            # fname = form_value.cleaned_data['fname']
            # email = form_value.cleaned_data['email']
            # telephone = form_value.cleaned_data['telephone']
            # if first_password == second_password:
            #     #添加到数据库
            #     User.objects.create(username= username,password=second_password,lname=lname,fname=fname,email=email,telephone=telephone)
            #     # return HttpResponse('regist success!!')
            #     logger.logger.info("%s regist success !"%username)
            logger.logger.info("[username] %s regist success !"%username)
            return render_to_response('login.html')
    else:
        form_value = UserForm()
    return render_to_response('login.html',{'form_value':form_value}, context_instance=RequestContext(request))
    # return render_to_response('regist.html',{'form_value':form_value}, context_instance=RequestContext(request))

#登陆
def login(request):
    if request.method == 'POST':
        print(request.POST)
        form_value = UserForm(request.POST)
        if form_value.is_valid():
            #获取表单用户密码
            username = form_value.cleaned_data['username']
            password = form_value.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/cmdb/home/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                # logger.logger.info("%s loggin !"%username)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/cmdb/login/')
    else:
        form_value = UserForm()
    return render_to_response('login.html')
    # return render_to_response('login.html',{'form_value':form_value},context_instance=RequestContext(request))

#退出
def logout(request):
    response = HttpResponseRedirect('/cmdb/login/')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response


def command(request):
    username = request.COOKIES.get('username','')
    # t_cmd = Command_info.objects.all()
    print(request.POST)
    if request.POST.get('action') == "Create":
        print(request.POST)
        cmd_name = request.POST.get('cmd_name')
        cmd_description = request.POST.get('cmd_description')
        cmd_demo = request.POST.get('cmd_demo')
        create_user = request.POST.get('create_user')
        if len(create_user) == 0:
            create_user = username
        cmd_args = request.POST.get('cmd_args')
        Command_info.objects.create(cmd_name= cmd_name,cmd_description=cmd_description,cmd_demo=cmd_demo,create_user=create_user,cmd_args=cmd_args)
    elif request.POST.get('action') == "Delete":
        d=Command_info.objects.get(cmd_id=request.POST.get('cmd_id'))
        d.delete()
    elif request.POST.get('action') == "Modify":
        print "Modify"
    elif request.POST.get('action') == "Select":
        #模糊查询，https://www.douban.com/note/301166150/
        #分页查询，http://www.cnblogs.com/holbrook/archive/2012/02/09/2357348.html
        t_value = Command_info.objects.all().filter(cmd_name__contains=request.POST.get('cmd_name'))
        p = Paginator(t_value, 1)
        print(p.object_list)
        page1 = p.page(1)
        print(t_value)
        return render_to_response('command.html',{'t_cmd':page1.object_list,'username':username})
    else:
        # t_cmd = Command_info.objects.all()
        pass
    t_cmd = Command_info.objects.all()
    return render_to_response('command.html',{'t_cmd':t_cmd,'username':username})

# def base(request):
#     return render_to_response('base.html')


def filemanage(request):
    return render_to_response('filemanage.html')


def test(request):
    if request.method == "POST":
        id = str(request.POST.get("id").strip("u''"))
    else:
        return render_to_response('test.html')
        #id = str(request.GET.get("id").strip("u''"))
    sql="SELECT t1.sku_id , t1.type , t1.jd_prc , t1.stk_prc , (t1.jd_prc - t1.stk_prc) / t1.jd_prc as ratio from gdm.gdm_m03_item_sku_price_da t1 where sku_id = '"+id+"' and dt = sysdate( - 1)"
    # prestoUrl = "http://bdpadhoc.jd.com:8888/presto/execute"
    prestoUrl = "http://127.0.0.1:8888/presto/execute"
    request = urllib2.Request(prestoUrl, data=sql)
    request.add_header('X-Presto-User', 'mart_vdp')  # presto 用户名
    request.add_header('X-Presto-Password', 'Ac8ZpCtKVj63mk2yAFmR') # presto 密码
    request.add_header('X-Presto-Catalog', 'mart_vdp_druid') # presto  catalog
    request.add_header('X-Presto-Schema', 'app') # catalog 下库名
    res = urllib2.urlopen(request)
    # 返回数据为 json 格式
    ret=res.read()
    # print ret
    #print json.loads(ret)['data'][0][1]
    #print json.dumps(json.loads(ret)['data']).strip("[]").split(",")
    #data={"sku_id":json.loads(ret)['data'][0],"type":json.loads(ret)['data'][1],"jd_prc":json.loads(ret)['data'][2],"stk_prc":json.loads(ret)['data'][3]}
    if len(json.loads(ret)['data'][0]) == 5:
        # data={"sku_id":json.loads(ret)['data'][0][0],"type":json.loads(ret)['data'][0][1],"jd_prc":json.loads(ret)['data'][0][2],"stk_prc":json.loads(ret)['data'][0][3]}
        print json.loads(ret)['data'][0][0]
        print json.loads(ret)['data'][0][1]
        print json.loads(ret)['data'][0][2]
        print json.loads(ret)['data'][0][3]
        return HttpResponse("sku_id:%s,jd_prc:%s,stk_prc:%s,stk_prc:%s"%(json.loads(ret)['data'][0][0],json.loads(ret)['data'][0][1],json.loads(ret)['data'][0][2],json.loads(ret)['data'][0][3]))
    else:
        return HttpResponse(ret)
