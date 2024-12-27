"""
群机器人发送
https://work.weixin.qq.com/api/doc/90000/90136/91770


{
    "msgtype": "markdown",
    "markdown": {
        "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
         >类型:<font color=\"comment\">用户反馈</font>
         >普通用户反馈:<font color=\"comment\">117例</font>
         >VIP用户反馈:<font color=\"comment\">15例</font>"
    }
}
"""
import logging
import os

import requests
from requests.exceptions import ConnectTimeout

logger = logging.getLogger(__name__)


def send_markdown(message_content, msg_to=None):
    logger.info("微信群聊机器人: message_content %s" % message_content)
    if msg_to is None:
        msg_to = ["@all"]
    body = {
        "msgtype": "markdown",
        "markdown": {"content": message_content},
        "mentioned_list": msg_to if msg_to else ["@all"],
    }
    WECHAT_ROBOT_ENDPOINT = os.environ.get("WECHAT_ROBOT_ENDPOINT", "")
    try:
        res = requests.post(WECHAT_ROBOT_ENDPOINT, json=body, timeout=30)
        assert res
        if res.status_code == 200 and res.json()["errcode"] == 0:
            logger.info("微信群聊机器人: 发送成功")
            return 1
        else:
            logger.info("微信群聊机器人: %s-%s" % (res.status_code, res.json()))
    except ConnectionError as e:
        logger.info("微信群聊机器人: connection error: %s" % e)
    except ConnectTimeout as e:
        logger.info("微信群聊机器人: time out： %s" % e)
    except Exception as e:
        logger.info("微信群聊机器人: send error: %s" % e)
    return 0
