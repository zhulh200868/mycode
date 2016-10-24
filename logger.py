#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging,os,sys
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)


#create logger
logger = logging.getLogger('SALT-LOG')
logger.setLevel(logging.DEBUG)


# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create file handler and set level to warning
if os.path.exists("%s/logs"%base_dir) is not True:
    os.mkdir("%s/logs"%base_dir)
# fh = logging.FileHandler("%s/logs/logger.log"%base_dir,"a")
fh = logging.FileHandler("E:/logger.log","a")
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)
