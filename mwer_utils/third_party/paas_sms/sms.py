# -*- coding: utf-8 -*-
# @Time : 2021/1/27 17:48
# @Author : shunzhou
# @Description: PAAS平台短信发送

import json
import logging
import os

import requests
from django.utils.functional import LazyObject
from requests.exceptions import ConnectTimeout

from sre_buff.constant import MONITOR_STATUS_CHOICE

logger = logging.getLogger(__name__)


class PaasSetting(object):
    def __init__(self):
        self.PAAS_SMS_ENDPOINT = os.environ.get("PAAS_SMS_ENDPOINT", "")
        self.PAAS_SMS_APPID = os.environ.get("PAAS_SMS_APPID", "")
        self.PAAS_SMS_SUCCESS_CODE = os.environ.get("PAAS_SMS_SUCCESS_CODE", "")
        self.PAAS_SMS_TPID_ALARM = os.environ.get("PAAS_SMS_TPID_ALARM", "")
        self.PAAS_SMS_TPID_RESOLVE = os.environ.get("PAAS_SMS_TPID_RESOLVE", "")
        self.PAAS_SMS_TEMPLATE_ALARM_FIELDS = os.environ.get(
            "PAAS_SMS_TEMPLATE_ALARM_FIELDS", []
        )
        self.PAAS_SMS_TEMPLATE_RESOLVE_FIELDS = os.environ.get(
            "PAAS_SMS_TEMPLATE_RESOLVE_FIELDS", []
        )


class PaasObject(LazyObject):
    def _setup(self):
        self._wrapped = PaasSetting()


class SmsSend:
    def __init__(self):
        self.setting = PaasObject()

    def sms_template(self, alert_status, **kwargs):
        """格式化sms_template"""
        if alert_status == MONITOR_STATUS_CHOICE.resolved:
            fields = self.setting.PAAS_SMS_TEMPLATE_RESOLVE_FIELDS
        else:
            fields = self.setting.PAAS_SMS_TEMPLATE_ALARM_FIELDS
        fields = json.loads(fields)
        data = dict()
        for field in fields:
            data[field] = kwargs.get(field, "")
        return json.dumps(data)

    def send_sms(self, phones, alert_status, **kwargs):
        """
        :param phones: 手机里面
        :param status: 恢复/告警
        :param kwargs:
        :return:
        """
        if alert_status == MONITOR_STATUS_CHOICE.resolved:
            tid = self.setting.PAAS_SMS_TPID_RESOLVE
        else:
            tid = self.setting.PAAS_SMS_TPID_ALARM
        data = dict(
            appid=self.setting.PAAS_SMS_APPID,
            phone=phones,
            tid=int(tid),
            tp=self.sms_template(alert_status, **kwargs),
        )
        try:
            res = requests.post(self.setting.PAAS_SMS_ENDPOINT, json=data, timeout=30)
            logger.info("短信发送: %s-%s" % (res.status_code, res.text))
            if (
                res.status_code == 200
                and res.json()["code"] == self.setting.PAAS_SMS_SUCCESS_CODE
            ):
                return res
            else:
                return res
            # TODO 记录发送记录方便追溯(shunzhou)
        except ConnectionError as e:
            logger.error("发送短信失败: 连接失败可能原因本地网络环境有问题-%s" % str(e))
        except ConnectTimeout as e:
            logger.error("发送短信失败: 连接超时30s-%s" % str(e))
        except Exception as e:
            logger.error("发送短信失败: %s" % str(e))
            return 0
