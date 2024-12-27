from sre_buff.utils.third_party.aicall.call import phone_send


class TestSmsSend:
    def test_phone_call(self):
        res = phone_send([136817149061], "你好, 2020")
        assert "retCode" in res.json()
        assert res.json()["retCode"] == "400001"
