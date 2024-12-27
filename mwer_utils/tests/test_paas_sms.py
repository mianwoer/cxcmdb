import json
from unittest import SkipTest

from rest_framework.status import HTTP_200_OK

from sre_buff.constant import MONITOR_STATUS_CHOICE
from sre_buff.utils.third_party.paas_sms.sms import SmsSend


class TestSmsSend:
    def test_sms_template(self, mocker):
        mocker.patch.dict(
            "os.environ", {"PAAS_SMS_TEMPLATE_RESOLVE_FIELDS": '["title"]'}
        )
        mocker.patch.dict(
            "os.environ", {"PAAS_SMS_TEMPLATE_ALARM_FIELDS": '["end_time"]'}
        )
        data = dict(
            start_time="2020-02-01 12:12:00",
            value=1,
            title="哈哈大幅度",
            instance="10.103.12.11",
            end_time="2020-02-01 12:12:00",
        )
        sms_util = SmsSend()
        x = sms_util.sms_template(MONITOR_STATUS_CHOICE.resolved, **data)
        assert json.dumps(dict(title=data["title"])) == x
        data_alarm = sms_util.sms_template("FIRING", **data)
        assert json.dumps(dict(end_time=data["end_time"])) == data_alarm

    def test_sms_send(self, mocker):
        sms_util = SmsSend()
        res = sms_util.send_sms(
            ["13681714906"],
            "FIRING",
            **dict(
                start_time="2020-02-01 12:12:00",
                value=1,
                title="哈哈大幅度",
                instance="10.103.12.11",
                end_time="2020-02-01 12:12:00",
            )
        )
        assert res
        assert res.status_code == HTTP_200_OK

        res = sms_util.send_sms(
            ["13681714906"],
            MONITOR_STATUS_CHOICE.resolved,
            **dict(
                start_time="2020-02-01 12:12:00",
                value=1,
                title="哈哈大幅度",
                instance="10.103.12.11",
                end_time="2020-02-01 12:12:00",
            )
        )
        assert res
