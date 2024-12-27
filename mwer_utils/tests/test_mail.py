import os

from django.conf import settings

from sre_buff.utils.third_party.mail.main_send import send_mail

# WARNING: @shunzhou 邮件的发送测试 因为没有注入正确的密码 所以都是发送不成功的


def test_mail_send():
    res = send_mail("哈哈", "sdfsdfsdfds", ["shunzhou@iflytek.com"])
    assert not res


def test_mail_attach_send():
    filename = "{}/utils/tests/test.txt".format(settings.APPS_DIR)
    f = open(filename, "w+")
    f.write("bilibili")
    f.close()
    res = send_mail("哈哈", "带附件的邮件", ["shunzhou@iflytek.com"], filename=filename)
    assert not res
    os.remove(filename)
