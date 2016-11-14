#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.db import models

# Create your models here.

class ServiceInfo(models.Model):
    service=models.CharField(max_length=200,verbose_name="产品线")
    cluster_name=models.CharField(max_length=200,verbose_name="集群名")
    install_path=models.CharField(max_length=200,blank=True,verbose_name="安装路径")

    def __str__(self):
        return self.service+"_"+self.cluster_name

class FileInfo(models.Model):
    service_info= models.ForeignKey(ServiceInfo)
    salt_path=models.CharField(max_length=200,unique=True,verbose_name="git路径")
    target_path=models.CharField(max_length=200,verbose_name="本地路径")
    auth=models.CharField(max_length=200,verbose_name="权限")
    user_group=models.CharField(max_length=200,verbose_name="属组")
    user=models.CharField(max_length=200,verbose_name="用户")
    md5=models.CharField(max_length=200,verbose_name="md5值")
    update_time=models.CharField(max_length=200,verbose_name="更新时间")

    def __str__(self):
        return self.salt_path

class OperationRecord(models.Model):
    salt_path=models.CharField(max_length=200,verbose_name="本地路径")
    action=models.CharField(max_length=200,verbose_name="动作")
    operate_time=models.CharField(max_length=200,verbose_name="操作时间")
    file_info_id=models.CharField(max_length=200,verbose_name="文件id")

    def __str__(self):
        return self.salt_path
