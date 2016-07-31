#!/usr/bin/env python
# -*- coding=utf8 -*-


import os
import re
import xlsxwriter
import sys
import collections

# salt 172.18.144.69 cmd.run "salt-call hdfs_capacity.hdfs_cap decare"
def check_capacity():
    value_dicts=collections.OrderedDict()
    ns_list=str(os.popen("cat /software/servers/hadoop-2.7.1/etc/hadoop/hdfs-site.xml|grep -A 1 dfs.nameservices|grep -v dfs.nameservices| awk -F '>|<' '{print $3}'").read().strip().split("\n")).strip("['']").split(",")
    for ns in ns_list:
        result=os.popen("su - hadp -c 'hadoop dfs -count -q hdfs://%s/user/*'"%ns).read()
        lists=[]
        for line in result.strip().split("\n"):
            temp_list = [i for i in re.split('\|+',line.strip().replace(" ","|")) if i !=' ']
            temp_value = str(int(temp_list[6])/1024/1024/1024)
            temp_list[6] = temp_value
            lists.append(temp_list[4:])
        value_dicts[ns]=sorted(lists, key=lambda temp:int(temp[2]),reverse=True)
    return value_dicts

def xml(value_dicts,cluster_name):
    workbook = xlsxwriter.Workbook ('/tmp/%s_hdfs.xlsx'%cluster_name)
    worksheet = workbook.add_worksheet ()
    worksheet.set_column ('E:E', 40)
    worksheet.set_column ('B:D', 15)
    worksheet.set_row(0,20)
    #设置格式
    header_format = workbook.add_format ({'bold': True,'bg_color':'#7CCD7C','border':1,'align': 'center','valign': 'vcenter'})
    value_format = workbook.add_format ({'border':1})
    menu_format = workbook.add_format ({'bold': True,'border':1,'bg_color':'red','align': 'center','valign': 'vcenter'})
    worksheet.write ('A1', u'ns',header_format)
    worksheet.write ('B1', u'目录个数',header_format)
    worksheet.write ('C1', u'文件个数',header_format)
    worksheet.write ('D1', u'容量(单位GB)',header_format)
    worksheet.write ('E1', u'用户目录',header_format)
    ind_num=2
    num=0
    for index,keys in enumerate(value_dicts.keys()):
        ind_num+=int(num)
        num=0
        for indexs,value in enumerate(value_dicts[keys]):
            worksheet.write ('B%s'%str(int(indexs)+ind_num), value[0],value_format)
            worksheet.write ('C%s'%str(int(indexs)+ind_num), value[1],value_format)
            worksheet.write ('D%s'%str(int(indexs)+ind_num), value[2],value_format)
            worksheet.write ('E%s'%str(int(indexs)+ind_num), value[3],value_format)
            num=int(indexs)+1
        if num-1 == 0:
            worksheet.write ('A%s'%str(ind_num), keys,menu_format)
        else:
            #合并单元格
            worksheet.merge_range(ind_num-1,0, ind_num+num-2,0,keys,menu_format)
    workbook.close()

def hdfs_cap(cluster_name):
    try:
        xml(check_capacity(),cluster_name)
    except Exception,e:
        return False
    else:
        return True

if __name__ == "__main__":
    cluster_name=sys.argv[1]
    xml(check_capacity(),cluster_name)