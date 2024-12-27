# coding=utf-8
import base64
import hashlib
import hmac
import logging
import os
import time
import urllib.parse

import requests
from requests.exceptions import ConnectionError, ConnectTimeout

from sre_buff.utils.third_party.dingding.constant import DINGDING_VERFIFY_TYPE_CHOICE
from sre_buff.utils.third_party.dingding.exception import (
    DingDingEndpointNotExistsException,
)

logger = logging.getLogger(__name__)

URL = (
    "https://oapi.dingtalk.com/robot/send?access_token"
    "=159beb2eee980a07c0e99d90d0f7e888a768ce3c8340629a08f3a8a410feab8a"
)


def sign(secret):
    # 钉钉加签
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign, timestamp


def send_dingding(msg):
    """
    curl 'https://oapi.dingtalk.com/robot/send?access_token
    =159beb2eee980a07c0e99d90d0f7e888a768ce3c8340629a08f3a8a410feab8a' \
       -H 'Content-Type: application/json' \
       -d '{"msgtype": "text","text": {"content": "告警就是我, 是不一样的烟火"}}'
    """
    DINGDING_ENDPOINT = os.environ.get("DINGDING_ENDPOINT", "")
    DINGDING_VERIFY = os.environ.get("DINGDING_VERIFY", "KEYWORD")
    DINGDING_SECRECT = os.environ.get("DINGDING_SECRECT", "")
    DINGDING_KEYWORD = os.environ.get("DINGDING_KEYWORD", "")
    if not DINGDING_ENDPOINT:
        raise DingDingEndpointNotExistsException("DINGDING_ENDPOINT 未配置")
    body = {"msgtype": "text", "text": {"content": msg}}
    try:
        if DINGDING_VERFIFY_TYPE_CHOICE.SIGN == DINGDING_VERIFY:
            signstr, timestamp = sign(DINGDING_SECRECT)
            url = "{}&timestamp={}&sign={}".format(
                DINGDING_ENDPOINT, timestamp, signstr
            )
        elif DINGDING_VERIFY == DINGDING_VERFIFY_TYPE_CHOICE.KEYWORD:
            url = DINGDING_ENDPOINT
            if DINGDING_KEYWORD not in body["text"]["content"]:
                body["text"]["content"] = (
                    "[{}]".format(DINGDING_KEYWORD) + body["text"]["content"]
                )
        else:
            url = DINGDING_ENDPOINT
        res = requests.post(url, json=body, timeout=30)
        logger.info("钉钉发送: %s-%s" % (res.status_code, res.json()))
        return res
    except ConnectionError as e:
        logger.info("钉钉发送: connection error: %s" % e)
    except ConnectTimeout as e:
        logger.info("钉钉发送: time out： %s" % e)
    except Exception as e:
        logger.info("钉钉发送: send error: %s" % e)
    return 0


# if __name__ == "__main__":
#     send_dingding("哈哈哈哈哈")
