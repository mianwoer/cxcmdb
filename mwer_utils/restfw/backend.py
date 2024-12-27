"""
2021/4/13 23:43
desc
"""
import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from sre_buff.utils.django_util import get_or_none
from sre_buff.utils.util_data import iflytek_sso_response_parse

logger = logging.getLogger(__name__)

User = get_user_model()


class SSOTicketBackend(ModelBackend):
    """
    SSO ticket backend
    此时的username 就是 sso ticket, password忽略
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        url = "{}?ticket={}&service={}".format(
            settings.SSO_VERIFY_URL, username, password
        )
        logger.info(
            "SSO REQUEST: %s, %s, %s" % (settings.SSO_VERIFY_URL, username, password)
        )
        res = requests.get(url=url, verify=False, timeout=settings.SSO_VERIFY_TIMEOUT)
        logger.info("SSO RESPONSE: %s, %s" % (res.status_code, res.text))
        parsed_data = iflytek_sso_response_parse(res.text)
        if parsed_data["res"] == 0:
            # logger.info("SSO VERIFY SUCCESS: %s" % parsed_data)
            username = parsed_data["data"]["username"]
            first_name = parsed_data["data"]["first_name"]
            email = username + "@iflytek.com"
            user = get_or_none(User, username=username)
            if not user:
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    password=settings.SSO_INIT_PASSWORD,
                )
        else:
            logger.error("SSO VERIFY FAIL: %s" % parsed_data)
        return user
