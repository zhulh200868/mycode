#!/usr/bin/env python
# -*- coding=utf8 -*-

from django.shortcuts import render,render_to_response,HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django import forms
from models import User
import logger

# Create your views here.

#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

#登陆成功
def home(request):
    username = request.COOKIES.get('username','')
    if username:
        logger.logger.info("%s loggin !"%username)
        return render_to_response('index.html',{'username':username})
    else:
         return render_to_response('login.html')


def autodeploy(request):
    return render_to_response('autodeploy.html')



# #注册
# def regist(request):
#     if request.method == 'POST':
#         form_value = UserForm(request.POST)
#         if form_value.is_valid():
#             #获得表单数据
#             username = form_value.cleaned_data['username']
#             password = form_value.cleaned_data['password']
#             #添加到数据库
#             User.objects.create(username= username,password=password)
#             # return HttpResponse('regist success!!')
#             logger.logger.info("%s regist success !"%username)
#             return render_to_response('login.html')
#     else:
#         form_value = UserForm()
#     return render_to_response('regist.html',{'form_value':form_value}, context_instance=RequestContext(request))

#登陆
def login(request):
    if request.method == 'POST':
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