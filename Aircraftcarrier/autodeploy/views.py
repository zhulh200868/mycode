#!/usr/bin/env python
# -*- coding=utf-8 -*-

from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# http://hustxiaoxian.lofter.com/post/1cc7b162_3a6d738

@csrf_exempt
def return_data(request):
    print request.POST
    return HttpResponse(True)