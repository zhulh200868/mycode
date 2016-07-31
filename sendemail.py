#!/usr/bin/env python
# -*- coding=utf8 -*-

from email.header import Header
import smtplib
from email.mime.multipart import MIMEMultipart #python2.4及之前版本该模块不是这样调用的，而是email.MIMEMultipart.MIMEMultipart(),下同
from email.mime.text import MIMEText



#邮件发送模块
def email_file(subject,content,log_file):
    # ISOTIMEFORMAT='%Y-%m-%d'
    # day = time.strftime( ISOTIMEFORMAT, time.localtime() )
    # subject = "%s_%s"%(theme,day)#邮件标题，这里我把标题设成了你所发的附件名
    # content = "%s_%s,详情见附件"%(theme,day)#邮件内容
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, _charset='utf-8'))
    msg['Subject'] = Header(subject,'utf-8')
    msg["From"]=Header("service<service@qq.com>",'utf-8')
    from_addr = 'service@qq.com'#发件人地址
    smtp_server = 'smtp.qq.local'#邮件服务器
    to_addr = ['123@qq.com','456@qq.com']#收件人地址
    #邮箱密码
    password = '123456'
    msg['To'] = ', '.join(to_addr)
    try:
        server = smtplib.SMTP(smtp_server,25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        msgText = MIMEText('%s'%msg,'html','utf-8')#你所发的文字信息将以html形式呈现
        msg.attach(msgText)
        att = MIMEText(open('%s'%log_file, 'rb').read(), 'base64', 'utf-8')#添加附件
        att["Content-Type"] = 'application/octet-stream'
        log_name = log_file.split("/")[-1]
        att["Content-Disposition"] = "attachment; filename=%s"%log_name
        msg.attach(att)
        server.sendmail(from_addr,to_addr,msg.as_string())  #发送邮件
        server.quit()
        return True
    except Exception,e:
        print str(e)
        return False

#邮件发送模块
def email(subject,content):
    try:
        #subject是主题，content是内容
        msg = MIMEText(_text=content, _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        #昵称
        msg["From"]=Header("service<service@qq.com>",'utf-8')
        #输入Email地址:
        from_addr = 'service@qq.com'
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.qq.local'
        # 输入收件人地址:
        to_addr = ['123@qq.com','456@qq.com']
        #SMTP协议默认端口是25
        server = smtplib.SMTP(smtp_server, 25)
        #邮箱密码
        password = '123456'
        server.set_debuglevel(1)
        msg['To'] = ', '.join(to_addr)
        server.login(from_addr, password)
        server.sendmail(from_addr,to_addr,msg.as_string())  #发送邮件
        server.quit()
        print 'email send success,the address is %s' %to_addr
        return True
    except Exception,e:
        print str(e)
        print 'email send failed.'
        return False


if __name__ == "__main__":
    pass