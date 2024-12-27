# -*- coding: utf-8 -*-
# @Time : 2021/1/27 21:22
# @Author : shunzhou
# @Description: 发送邮件

import logging
import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPDataError

logger = logging.getLogger(__name__)


def send_mail(sub, content, tolist, content_type="plain", filename=""):
    """
    发送告警邮件
    :param sub: 主题
    :param content: 内容
    :param tolist: 发送对象
    :param content_type: 发送类型支持 plain/htmml
    :param filename: 文件路径
    :return:
    """
    mail_host = os.environ.get("MAIL_HOST", "")
    mail_user = os.environ.get("MAIL_SENDER_USER", "")
    mail_pass = os.environ.get("MAIL_SENDER_PASS", "")
    mail_port = os.environ.get("MAIL_PORT", "")
    me = "%s<%s>" % (Header(os.environ.get("MAIL_HEADER", ""), "utf-8"), mail_user)
    if filename:
        msg = MIMEMultipart()
        # 构建正文
        part_text = MIMEText(content, _subtype=content_type, _charset="utf-8")
        # 把正文加到邮件体里面去
        msg.attach(part_text)

        # TODO: 构建邮件附件
        if "xlsx" in filename:
            subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            subtype = "octet-stream"

        part_attach1 = MIMEApplication(open(filename, "rb").read(), _subtype=subtype)
        part_attach1.add_header(
            "Content-Disposition",
            "attachment",
            filename=("gbk", "", filename.split("/")[-1]),
        )  # 为附件命名
        msg.attach(part_attach1)  # 添加附件
    else:
        msg = MIMEText(content, _subtype=content_type, _charset="utf-8")
    msg["Subject"] = sub
    msg["From"] = me
    msg["To"] = ";".join(tolist)
    try:
        server = smtplib.SMTP(port=mail_port)
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, tolist, msg.as_string())
        server.close()
        logger.info("发送邮件成功")
        return 1
    except SMTPConnectError as e:
        logger.error("发送邮件失败: %s" % str(e))
    except SMTPAuthenticationError as e:
        logger.error("发送邮件失败: %s" % str(e))
    except SMTPDataError as e:
        logger.error("发送邮件失败: %s" % str(e))
    except Exception as e:
        logger.error("发送邮件失败: %s" % str(e))
    return 0
