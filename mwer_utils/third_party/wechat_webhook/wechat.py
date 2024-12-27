#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/14 20:51
# @Author  : Weizhang
# @File    :  wechat.py
# @Software: PyCharm


import json
import logging

import requests
from django.conf import settings

corpid = getattr(settings, "WECHAT_CORPID")
appsecret = getattr(settings, "WECHAT_APPSECRET")
agentid = getattr(settings, "WECHAT_AGENTID")
aces_url = getattr(settings, "WECHAT_TOKEN_URL")
msg_url = getattr(settings, "WECHAT_MSGSEND_URL")


def _get_access_url():
    return aces_url.strip() + "=" + corpid + "&corpsecret=" + appsecret


def sendmsg(tousers, data):
    """
    :param tousers:  用户微信号，多个用“|”进行区分
    :param data:
    :return:
    """
    # todo 获取accesstoken
    token_url = _get_access_url()
    req = requests.get(token_url)
    accesstoken = req.json()["access_token"]
    msgsend_url = msg_url.strip() + "=" + accesstoken

    params = {
        "touser": tousers,
        # "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {"content": data},
        "safe": 0,
    }
    try:
        req = requests.post(msgsend_url, data=json.dumps(params))
        logging.info("告警消息发送返回状态码: {}".format(str(req.status_code)))
        return req.status_code
    except Exception as e:
        logging.error(str(e))
