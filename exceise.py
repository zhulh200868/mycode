#!/usr/bin/env python
# -*- coding=utf8 -*-

"""
获取当前文件名、当前函数名、当前行号
"""
# import sys
# def get_cur_info():
#     print sys._getframe().f_code.co_filename # 当前文件名，可以通过__file__获得
#     print sys._getframe().f_code.co_name # 当前函数名
#     print sys._getframe().f_lineno # 当前行号
# get_cur_info()

"""
You want to write data to a file,but only if it don't already exist on the filesystem.
"""
##On the Python3
# with open("E:/Python/workspace/mycode/test.txt","xt") as f:
#     f.write("hello")

##On the Python2
# import os
# if not os.path.exists("E:/Python/workspace/mycode/test.txt"):
#     with open("E:/Python/workspace/mycode/test.txt","wt") as f:
#         f.write("hello")
# else:
#     print("File is already exits!")














