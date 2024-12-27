#! /usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
from django.contrib.auth.hashers import make_password
# from __future__ import unicode_literals
from django.db import models

# from appconf.models import AuthInfo

ASSET_STATUS = (
    (str(1), "使用中"),
    (str(2), "未使用"),
    (str(3), "故障"),
    (str(4), "其它"),
)

ASSET_TYPE = (
    (str(1), "物理机"),
    (str(2), "虚拟机"),
    (str(3), "容器"),
    (str(4), "网络设备"),
    (str(5), "安全设备"),
    (str(6), "其他")
)


class UserInfo(models.Model):
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.username


class Idc(models.Model):
    ids = models.CharField("机房标识", max_length=255, unique=True)
    name = models.CharField("机房名称", max_length=255, unique=True)
    address = models.CharField("机房地址", max_length=100, blank=True)
    tel = models.CharField("机房电话", max_length=30, blank=True)
    contact = models.CharField("客户经理", max_length=30, blank=True)
    contact_phone = models.CharField("移动电话", max_length=30, blank=True)
    jigui = models.CharField("机柜信息", max_length=30, blank=True)
    ip_range = models.CharField("IP范围", max_length=30, blank=True)
    bandwidth = models.CharField("接入带宽", max_length=30, blank=True)
    memo = models.TextField("备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name


# 项目表
class Project(models.Model):
    name = models.CharField(max_length=64, verbose_name="项目名称", unique=True)
    type = models.CharField("项目类型", max_length=32, null=True, blank=True)
    Customer_Unit = models.CharField("客户单位", max_length=64, null=True, blank=True)
    Customer_group = models.CharField(max_length=64, verbose_name="客群类型", null=True, blank=True)


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name="主机名", unique=True)
    ip = models.GenericIPAddressField("业务IP", max_length=15, null=True, blank=True)
    # account = models.ForeignKey(AuthInfo, verbose_name="账号信息", on_delete=models.SET_NULL, null=True, blank=True)
    idc = models.ForeignKey(Idc, verbose_name="所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    other_ip = models.CharField("BMC以及其它IP", max_length=100, null=True, blank=True)
    asset_no = models.CharField("资产编号", max_length=50, null=True, blank=True)
    asset_type = models.CharField("设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField("操作系统", max_length=100, null=True, blank=True)
    os_user = models.CharField("操作系统用户", max_length=50, null=True, blank=True)
    os_passwd = models.CharField("操作系统的密码", max_length=128, null=True, blank=True)  # 存储哈希后的密码
    vendor = models.CharField("设备厂商", max_length=50, null=True, blank=True)
    up_time = models.CharField("上架时间", max_length=50, null=True, blank=True)
    cpu_model = models.CharField("CPU型号", max_length=100, null=True, blank=True)
    cpu_num = models.CharField("CPU数量", max_length=100, null=True, blank=True)
    memory = models.CharField("内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField("硬盘信息", max_length=255, null=True, blank=True)
    sn = models.CharField("SN号 码", max_length=60, null=True, blank=True)
    position = models.CharField("所在位置", max_length=100, null=True, blank=True)
    memo = models.TextField("备注信息", max_length=200, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name="所属项目", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.hostname

    def set_os_passwd(self, raw_password):
        """操作系统密码字段的设置和校验"""
        self.os_passwd = make_password(raw_password)

    def check_os_passwd(self, raw_password):
        return self.os_passwd == make_password(raw_password)

    def test_ssh(self, port=22):
        """通过传入 os（linux系统） 的用户、密码 进行登录验证，返回json含是否成功信息 """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, port, self.os_user, self.os_passwd)
            return {"result": True,
                    "error": None}
        except Exception as e:
            raise {"result": False,
                   "error": e}
        finally:
            # 关闭连接
            ssh.close()


class Cabinet(models.Model):
    idc = models.ForeignKey(Idc, verbose_name="所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField("机柜", max_length=100)
    desc = models.CharField("描述", max_length=100, blank=True)

    serverList = models.ManyToManyField(
        Host,
        blank=True,
        verbose_name="所在服务器"
    )

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField("服务器组名", max_length=30, unique=True)
    desc = models.CharField("描述", max_length=100, blank=True)

    serverList = models.ManyToManyField(
        Host,
        blank=True,
        verbose_name="所在服务器"
    )

    def __str__(self):
        return self.name


class IpSource(models.Model):
    net = models.CharField(max_length=30)
    subnet = models.CharField(max_length=30, null=True)
    describe = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.net


class InterFace(models.Model):
    name = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30, null=True)
    bandwidth = models.CharField(max_length=30, null=True)
    tel = models.CharField(max_length=30, null=True)
    contact = models.CharField(max_length=30, null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    price = models.IntegerField(verbose_name=u'价格')

    def __str__(self):
        return self.name
