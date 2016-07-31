#!/usr/bin/env python
# -*- coding=utf8 -*-

import pexpect
import getpass
'''
通过scp命令传输文件
'''
host=raw_input('hostname: ')
remote_path=raw_input('remote_path: ')
local_file=raw_input('local_file: ')
passwd=getpass.getpass('password: ')
cmd='scp -r %s %s:%s'%(local_file,host,remote_path)
child=pexpect.spawn(cmd)
child.expect('password:')
child.sendline(passwd)
child.read()