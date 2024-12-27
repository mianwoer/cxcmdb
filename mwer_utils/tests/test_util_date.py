"""
2021/5/8 12:02
desc
"""
from datetime import datetime

from sre_buff.utils.util_date import (
    dateday_range,
    dateday_str,
    datemonth_range,
    datemonth_str,
    datestr_datetime,
    dateweek_range,
    dateweek_str,
)


def test_datestr_datetime():
    assert datestr_datetime("20210525") == datetime(2021, 5, 25)


def test_dateday_str():
    assert dateday_str(datetime(2021, 5, 8)) == "20210508"
    assert dateday_str(datetime(2021, 5, 28)) == "20210528"


def test_datemonth_str():
    assert datemonth_str(datetime(2021, 5, 8)) == "202105"
    assert datemonth_str(datetime(2021, 12, 28)) == "202112"


def test_dateweek_str():
    assert dateweek_str(datetime(2021, 5, 8)) == "202119"
    assert dateweek_str(datetime(2021, 1, 1)) == "202101"


def test_dateday_range():
    assert dateday_range(datetime(2021, 5, 8)) == [
        datetime(2021, 5, 8, 0, 0, 0),
        datetime(2021, 5, 9, 0, 0, 0),
    ]

    assert dateday_range(datetime(2021, 12, 31)) == [
        datetime(2021, 12, 31, 0, 0, 0),
        datetime(2022, 1, 1, 0, 0, 0),
    ]


def test_datemonth_range():
    assert datemonth_range(datetime(2021, 5, 8)) == [
        datetime(2021, 5, 1, 0, 0, 0),
        datetime(2021, 6, 1, 0, 0, 0),
    ]
    assert datemonth_range(datetime(2021, 12, 8)) == [
        datetime(2021, 12, 1, 0, 0, 0),
        datetime(2022, 1, 1, 0, 0, 0),
    ]


def test_dateweek_range():
    assert dateweek_range(datetime(2021, 5, 8)) == [
        datetime(2021, 5, 3, 0, 0, 0),
        datetime(2021, 5, 10, 0, 0, 0),
    ]

    assert dateweek_range(datetime(2021, 1, 1)) == [
        datetime(2020, 12, 28, 0, 0, 0),
        datetime(2021, 1, 4, 0, 0, 0),
    ]
