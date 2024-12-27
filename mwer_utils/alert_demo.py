"""发送qq邮件代码demo"""
# 无需安装第三方库
key = 'lwmgyrtjstqpdjdi'  # 换成你的QQ邮箱SMTP的授权码(QQ邮箱设置里)
SenderMail = '2547319194@qq.com'  # 换成你的邮箱地址
ReceiverMail = 'zhuliu4@kxdigit.com'
EMAIL_PASSWORD = key

import smtplib

smtp = smtplib.SMTP('smtp.qq.com', 25)

import ssl

context = ssl.create_default_context()
sender = SenderMail  # 发件邮箱
receiver = ReceiverMail
# 收件邮箱
from email.message import EmailMessage

subject = "python email subject"
body = "Hello,this is an email sent by python!"
msg = EmailMessage()
msg['subject'] = subject  # 邮件主题
msg['From'] = sender
msg['To'] = receiver
msg.set_content(body)  # 邮件内容

with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
    smtp.login(SenderMail, EMAIL_PASSWORD)
    smtp.send_message(msg)
