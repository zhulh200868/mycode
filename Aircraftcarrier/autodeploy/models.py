#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.db import models

# Create your models here.

class t_exec_error_log(models.Model):
    pass
class t_exec_jid_detail():
    jid = models.CharField(max_length=30,verbose_name="任务ID")
    ip = models.CharField(max_length=15,verbose_name="服务器IP")
    result = models.CharField(max_length=10,verbose_name="执行结果")
    detail = models.CharField(max_length=2000,verbose_name="详细")
    donetime = models.CharField(max_length=200,verbose_name="完成时间")
    def __str__(self):
        return self.jid+"_"+self.ip+"_"+self.result

class t_exec_log():
    pass

class t_exec_mapping():
    pass