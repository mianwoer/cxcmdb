import json
import os

import pytest
from django.conf import settings

from sre_buff.utils.tests.mocks import (
    IFLYTE_SSO_VERIFY_FAIL_RESULT,
    IFLYTE_SSO_VERIFY_RAISE_RESULT,
    IFLYTE_SSO_VERIFY_SUCCESS_RESULT,
)
from sre_buff.utils.util_data import (
    check_int,
    data_for_excel,
    email_check,
    excel_write,
    iflytek_sso_response_parse,
    is_sub_dict,
    match_ip,
    match_url,
    phone_check,
    read_excel,
    read_json_file,
)


class TestUtilData:
    def test_email_check(self):
        e1 = "sfsdf"
        assert not email_check(e1)
        e2 = "sdf@iflytek.com"
        assert email_check(e2)
        e3 = "sdfs@@iflytek.com"
        assert not email_check(e3)
        e4 = "士大夫@eee.com"
        assert email_check(e4)
        e5 = "linux-c@qq.com"
        assert email_check(e5)

    def test_phone_check(self):
        p1 = "12132131231"
        assert not phone_check(p1)
        p2 = "12312334"
        assert not phone_check(p2)
        p3 = "13681714906"
        assert phone_check(p3)
        p4 = "14681714906"
        assert phone_check(p4)
        p5 = "15681714906"
        assert phone_check(p5)

    def test_read_json_file(self):
        data = read_json_file("{}/utils/tests/jsonfile.json".format(settings.APPS_DIR))
        assert isinstance(data, dict)

    def test_iflytek_sso_parse_raise(self):
        data = iflytek_sso_response_parse(IFLYTE_SSO_VERIFY_RAISE_RESULT)
        assert data["res"] == 1
        assert data["msg"] == "parse raise error"

    def test_iflytek_sso_parse_fail(self):
        data = iflytek_sso_response_parse(IFLYTE_SSO_VERIFY_FAIL_RESULT)
        assert data["res"] == 1
        assert (
            data["msg"]
            == "Ticket 'ST-22425-ELpHsQUuRZOYO4bhCPIkEO5Kpg4-ssodev1' not recognized"
        )

    def test_iflyte_sso_parse_success(self):
        data = iflytek_sso_response_parse(IFLYTE_SSO_VERIFY_SUCCESS_RESULT)
        assert data["res"] == 0
        assert data["data"]["username"] == "qizhu2"
        assert data["data"]["first_name"] == "朱琪"

    def test_read_not_json_file(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            read_json_file("{}/utils/tests/notjsonfile.json".format(settings.APPS_DIR))

    def test_read_json_file_no_exists(self):
        with pytest.raises(FileExistsError):
            read_json_file("xxx")

    def test_check_int(self):
        assert check_int("0")
        assert check_int("1212")
        assert not check_int("sdf")

    def test_match_ip(self):
        str0 = "_10.103.15.16-dfdfd"
        assert "10.103.15.16" == match_ip(str0)

        str1 = "ipackage-server_10.103.15.16"
        assert "10.103.15.16" == match_ip(str1)

        str2 = "ipackage-server_10.103.15.461"
        assert "" == match_ip(str2)

        str3 = "ipackage-server_10."
        assert "" == match_ip(str3)

        str4 = "10.103.15.16"
        assert "10.103.15.16" == match_ip(str4)

    def test_web_url(self):
        str0 = "https://www.baidu.com:443/api"

        assert "https://www.baidu.com:443/api" == match_url(str0)

        str1 = "sdfsdfs-https://www.baidu.com:443/api"
        assert "https://www.baidu.com:443/api" == match_url(str1)

        str2 = "sdfsdfs-https://www.baidu.com:443/api dfsdfs"
        assert "https://www.baidu.com:443/api" == match_url(str2)

    def test_data_for_excel(self):
        datas = [
            {"key1": "value1", "key2": "value2"},
            {"key1": "value3", "key2": "value4"},
        ]
        result = data_for_excel(datas)
        assert result == [["key1", "key2"], ["value1", "value2"], ["value3", "value4"]]

        datas = [
            {"key1": "value2", "key2": "value1"},
            {"key1": "value3", "key2": "value4"},
        ]
        result = data_for_excel(datas)
        assert result == [["key1", "key2"], ["value2", "value1"], ["value3", "value4"]]

        datas = [
            {"key2": "value1", "key1": "value2"},
            {"key1": "value3", "key2": "value4"},
        ]
        result = data_for_excel(datas)
        assert result == [["key2", "key1"], ["value1", "value2"], ["value4", "value3"]]

    def test_excel_write(self):
        datas = [["a", "B"], [1, 2]]
        filename = "{}/utils/tests/execl.xlsx".format(settings.APPS_DIR)
        x = excel_write(filename, datas)
        assert x
        y = read_excel(filename)
        assert y == datas
        os.remove(filename)

    def test_excel_write_dict_arrays(self):
        datas = [{"A": "TITLE", "B": "VALUE"}, {"A": 3, "B": 4}]
        filename = "{}/utils/tests/execl.xlsx".format(settings.APPS_DIR)
        x = excel_write(filename, datas)
        assert x
        y = read_excel(filename)
        assert y == [["TITLE", "VALUE"], [3, 4]]
        os.remove(filename)

    def test_is_sub_dict(self):
        a = {
            "env": "生产环境",
            "role": "ibuild",
            "level": "2",
            "instance": "CI/IBUILD-Jenkins-node_10.103.57.24",
            "severity": "notice",
            "alertname": "cpu.user40",
            "system_name": "iBuild",
        }
        b = {"env": "生产环境", "role": "ibuild", "level": "2"}
        assert is_sub_dict(a, b)
        c = {"level": "2"}
        assert is_sub_dict(a, c)
        d = {"level": "1"}
        assert not is_sub_dict(a, d)
