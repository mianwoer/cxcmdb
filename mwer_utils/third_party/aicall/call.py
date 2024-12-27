# -*- coding: utf-8 -*-
# @Time : 2021/1/29 9:17
# @Author : shunzhou
# @Description:

import hmac
import json
import logging
import os
from hashlib import sha1

import requests
from django.utils.functional import LazyObject

logger = logging.getLogger(__name__)


class AICallSetting(object):
    def __init__(self):
        self.CALL_CONSUMER_Id = os.environ.get("CALL_CONSUMER_Id", "")
        self.CALL_TASK_Id = os.environ.get("CALL_TASK_Id", "")
        self.CALL_CONSUMER = os.environ.get("CALL_CONSUMER", "")
        self.CALL_ENDPOINT = os.environ.get("CALL_ENDPOINT", "")
        self.CALL_HASH_KEY = os.environ.get("CALL_HASH_KEY", "")
        self.CALL_PREFIX = os.environ.get("CALL_PREFIX", "四级系统告警")


class AICallObject(LazyObject):
    def _setup(self):
        self._wrapped = AICallSetting()


def hash_hmac(key, code, sha1):
    hmac_code = hmac.new(key.encode(), code.encode("utf8"), sha1)
    return hmac_code.hexdigest()


def request_phone(consumerId, taskId, consumer, phones, content, hash_key, url):
    phones_list = [int(i) for i in phones]
    str = u'consumer=%s&consumerId=%s&phones=%s&props={"content":"%s"}&taskId=%s' % (
        consumer,
        consumerId,
        phones_list,
        content,
        taskId,
    )
    # 生成校验签名(必传)
    sign = hash_hmac(hash_key, str, sha1)
    # 生成POST传参内容
    send_content = {
        "taskId": taskId,
        "phones": phones,
        "consumerId": consumerId,
        "consumer": consumer,
        "props": {"content": content},
        "sign": sign,
    }
    headers = {"Content-Type": "application/json"}
    data = json.dumps(send_content, ensure_ascii=False)
    resp = requests.post(url, headers=headers, data=data.encode("utf-8"))
    return resp


def phone_send(phones, message):
    aicall = AICallObject()
    content = u"{}:".format(aicall.CALL_PREFIX) + message + " " + message
    send_resp = request_phone(
        aicall.CALL_CONSUMER_Id,
        aicall.CALL_TASK_Id,
        aicall.CALL_CONSUMER,
        phones,
        content,
        aicall.CALL_HASH_KEY,
        aicall.CALL_ENDPOINT,
    )
    logger.info("电话告警: %s" % send_resp.text)
    return send_resp
