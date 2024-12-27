from unittest import SkipTest

from third_party.elk.connect import LogSourceElk


class TestLogSourceCase:
    # ('elasticsearch耗资源')
    @SkipTest
    def test_connect(self):
        lselk = LogSourceElk("elk:9200")
        assert lselk.status()
