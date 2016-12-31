#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging.config
import logging,os,sys
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler


base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
# create file handler and set level to warning
if os.path.exists("%s/logs"%base_dir) is not True:
    os.mkdir("%s/logs"%base_dir)

class Log_Rota(object):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s",
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'cloghandler.ConcurrentRotatingFileHandler',
                # 当达到10MB时分割日志
                'maxBytes': 1024 * 1024 *100,
                # 最多保留50份文件
                'backupCount': 50,
                # If delay is true,
                # then file opening is deferred until the first call to emit().
                'delay': True,
                'filename': 'logs/myscript.log',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'INFO',
            },
        }
    })

    logger = logging.getLogger('myscript')

class Log_Time(object):
    logname = '%s/logs/myscript.log'%base_dir

    #是否要打印在屏幕#
    is_console=True
    #是否要备份日志#
    is_backfile=False
    #是否写日志#
    is_writefile = True

    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
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
    if is_writefile:
        logfile =  TimedRotatingFileHandler("%s"%logname, "D", 1, 10)
        logfile.suffix = "%Y%m%d"
        formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
        logfile.setLevel(logging.INFO)
        logfile.setFormatter(formatter)
        logger.addHandler(logfile)



