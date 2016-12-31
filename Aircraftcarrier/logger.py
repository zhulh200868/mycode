#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging.config

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
            'filename': 'logs/aircraftcarrier.log',
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



