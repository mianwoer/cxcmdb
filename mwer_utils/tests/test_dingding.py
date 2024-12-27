from unittest import mock

import pytest

from sre_buff.utils.third_party.dingding import (
    DingDingEndpointNotExistsException,
    send_dingding,
)


def test_dingding_send():
    assert send_dingding("哈哈哈哈")


def test_dingding_endpoint():
    with mock.patch.dict("os.environ", {"DINGDING_ENDPOINT": ""}, clear=True):
        with pytest.raises(DingDingEndpointNotExistsException):
            send_dingding("sdfsdf")
