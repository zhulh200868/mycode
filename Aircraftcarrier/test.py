#!/usr/bin/env python
# -*- coding=utf8 -*-

from multiprocessing import Pool
import time
import MySQLdb

class Monitor(object):
    def __init__(self):
        pass

    def monitors(self):
        print models.t_exec_jid_detail.objects.all()


if __name__ == "__main__":
    m = Monitor()
    m.monitors()
