#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging,os,sys
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler


#是否要打印在屏幕#
is_console=True
#是否要备份日志#
is_backfile=False
#是否写日志#
is_writefile = True

# create file handler and set level to warning
if os.path.exists("%s/logs"%base_dir) is not True:
    os.mkdir("%s/logs"%base_dir)
logname = '%s/logs/myscript.log'%base_dir
# logname = "myapp.log"

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

# logging.basicConfig(level=logging.DEBUG,)
# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='%s'%logname,
#                     filemode='w')
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
if is_console:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # logging.getLogger('').addHandler(console)
#################################################################################################
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
if is_backfile:
    Rthandler = RotatingFileHandler('%s'%logname,maxBytes=100*1024*1024,backupCount=5)
    Rthandler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)
    # logging.getLogger('').addHandler(Rthandler)
#################################################################################################
#定义一个FileHandler，将INFO级别或更高的日志信息写入日志中#
# if is_writefile:
#     logfile = logging.FileHandler("%s"%logname,'w')
#     logfile.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
#     logfile.setFormatter(formatter)
#     logger.addHandler(logfile)
if is_writefile:
    logfile =  TimedRotatingFileHandler("%s"%logname, "D", 1, 10)
    logfile.suffix = "%Y%m%d"
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    logfile.setLevel(logging.INFO)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
