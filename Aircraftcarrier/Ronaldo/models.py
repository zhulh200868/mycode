#!/usr/bin/env python
# -*- coding=utf-8 -*-
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    # lname = models.CharField(max_length=50)
    # fname = models.CharField(max_length=50)
    # email = models.CharField(max_length=50)
    # telephone = models.CharField(max_length=50)
    def __unicode__(self):
        return self.username

class Command_info(models.Model):
    cmd_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='cmd_id')
    cmd_name = models.CharField(max_length=200,null=True,blank=True,unique=True,verbose_name="命令名称")
    cmd_description = models.CharField(max_length=2000,null=True,blank=True,verbose_name="命令描述")
    create_user = models.CharField(max_length=200,null=True,blank=True,verbose_name="创建者")
    create_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name="创建时间")
    state = models.IntegerField(null=True,blank=True,verbose_name="状态")
    cmd_args = models.TextField(max_length=4000,null=True,blank=True,verbose_name="参数")
    modify_date = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name="修改时间")
    modify_user = models.CharField(max_length=200,null=True,blank=True,verbose_name="修改者")
    cmd_demo = models.TextField(max_length=4000,null=True,blank=True,verbose_name="名称示例")
    def __unicode__(self):
        return self.cmd_name
