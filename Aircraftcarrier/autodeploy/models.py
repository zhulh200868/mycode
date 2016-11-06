#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.db import models

# Create your models here.

class t_exec_error_log(models.Model):
    # id = models.BigIntegerField(max_length=20,auto_created=True)
    create_date = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    error_info = models.TextField(max_length=4000,verbose_name="错误信息")
    no = models.IntegerField(verbose_name="单号")
    task_id = models.CharField(max_length=50,verbose_name="任务号")

    def __str__(self):
        return self.task_id

class t_exec_jid_detail(models.Model):
    # id = models.BigIntegerField(max_length=20,auto_created=True)
    jid = models.CharField(max_length=30,verbose_name="任务ID")
    ip = models.CharField(max_length=15,verbose_name="服务器IP")
    result = models.CharField(max_length=10,verbose_name="执行结果")
    detail = models.TextField(max_length=4000,verbose_name="详细")
    donetime = models.DateTimeField(auto_now_add=True,verbose_name="完成时间")
    def __str__(self):
        return self.jid+"_"+self.ip+"_"+self.result

class t_exec_log(models.Model):
    # id = models.BigIntegerField(max_length=20,auto_created=True)
    task_id = models.CharField(max_length=50,verbose_name="任务号")
    def __str__(self):
        return self.id+"_"+self.task_id
class t_exec_mapping(models.Model):
    jid = models.CharField(max_length=30,verbose_name="任务ID")
    ip_list = models.TextField(max_length=4000,verbose_name="IP列表")
    command = models.CharField(max_length=50,verbose_name="命令")
    no = models.IntegerField(verbose_name="单号")
    task_id = models.CharField(max_length=50,verbose_name="任务号")
    def __str__(self):
        return self.jid+"_"+self.ip_list+"_"+self.command
