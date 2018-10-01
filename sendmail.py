#! /usr/bin/env python3
# -*- coding:utf-8 -*-


__author__ = 'Chen Yansu'

'''
一个邮件系统
只要传题目和正文，即可发送邮件
'''

import os
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from threading import Thread


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail(mail_subject, mail_content=None):
    from_addr = os.environ.get('MAIL_USERNAME')
    to_addr = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    smtp_server = 'smtp.sina.com'

    msg = MIMEText('%s' % mail_content, 'plain', 'utf-8')
    msg['Subject'] = Header(u'%s' % mail_subject, 'utf-8').encode()
    msg['From'] = _format_addr(u'陈严肃的自动发送邮件 <%s>' % from_addr)
    msg['To'] = _format_addr(u'陈严肃 <%s>' % to_addr)

    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_async_mail(mail_subject, mail_content=None):
    thr = Thread(target=send_mail, args=[mail_subject,mail_content])
    thr.start()
    return thr


# if __name__ == "__main__":
#     # ssss = Send_mail(the_subject='the_thrid_test', the_content='It is good')
#     # ssss.send_start()
#     send_mail(mail_subject='the_thrid_test', mail_content='It is good')
