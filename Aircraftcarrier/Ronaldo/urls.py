"""Aircraftcarrier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import home,login,logout,autodeploy,regist,command,test,filemanage,dns,hello

urlpatterns = [
    url(r'^home/$',home, name='home'),
    url(r'^login/$',login, name='login'),
    url(r'^logout/$',logout,name = 'logout'),
    url(r'^regist/$',regist,name = 'regist'),
    url(r'^autodeploy/$',autodeploy, name='autodeploy'),
    url(r'^command/$',command, name='command'),
    url(r'^filemanage/$',filemanage, name='filemanage'),
    url(r'^dns/$',dns, name='dns'),
    # url(r'^home/base/$',base, name='base'),
    url(r'^test/$',test, name='test'),
    url(r'^hello/$',hello, name='hello'),
]
