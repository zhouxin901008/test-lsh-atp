# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class sendMail:
    def mail(self,resultTime):
        sender = 'zxin901008@163.com'
        receivers = ['zxin901008@163.com']


        message = MIMEMultipart()
        message['From'] = Header("zxin901008@163.com", 'utf-8')
        message['To'] =  Header("zxin901008@163.com", 'utf-8')

        subject = '测试'
        message['Subject'] = Header(subject, 'utf-8')

        message.attach(MIMEText('交易系统库存测试结果...', 'plain', 'utf-8'))

        att1 = MIMEText(open('/Users/zhouxin/PycharmProjects/testinterface/atpTestCase/atpTestResult_' + resultTime + '.xls', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="atpTestResult_' + resultTime + '.xls"'
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect('smtp.163.com', 25)
            smtpObj.login(sender, 'xyz20070611')
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print "邮件发送成功"
        except smtplib.SMTPException,e:
            print "Error: 无法发送邮件",e