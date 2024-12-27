"""
2021/5/8 11:22
desc  跟时间相关的函数
"""
from datetime import datetime, timedelta


def datestr_datetime(datestr):
    return datetime.strptime(datestr, "%Y%m%d")


def dateday_str(date=datetime(2021, 4, 1)):
    """通过给定日期返回 20210501"""
    return date.strftime("%Y%m%d")


def datemonth_str(date=datetime(2021, 4, 1)):
    """ 通过给定日期返回 此日期的年和第几月"""
    return date.strftime("%Y%m")


def dateweek_str(date=datetime(2021, 4, 1)):
    """通过给定日期返回 此日期的年和第几周"""

    return str(int(date.strftime("%Y%W")) + 1)


def datemonth_range(date=datetime(2021, 4, 1)):
    """ 通过给定日期， 返回当前月的起始"""
    year, month = date.year, date.month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return [
        datetime(year, month, 1, 0, 0, 0),
        datetime(next_year, next_month, 1, 0, 0, 0),
    ]


def dateweek_range(date=datetime(2021, 4, 1)):
    """ 通过给定日期， 返回当前月的起始 """
    weeday_current = date.weekday()
    weekday_first = date - timedelta(days=weeday_current)
    weekday_last = weekday_first + timedelta(days=7)
    return [
        datetime(weekday_first.year, weekday_first.month, weekday_first.day, 0, 0, 0),
        datetime(weekday_last.year, weekday_last.month, weekday_last.day, 0, 0, 0),
    ]


def dateday_range(date=datetime(2021, 4, 1)):
    """ 通过给定日期， 返回当前月的起始"""
    year, month, day = date.year, date.month, date.day
    next_year, next_month, next_day = (
        (date + timedelta(days=1)).year,
        (date + timedelta(days=1)).month,
        (date + timedelta(days=1)).day,
    )
    return [
        datetime(year, month, day, 0, 0, 0),
        datetime(next_year, next_month, next_day, 0, 0, 0),
    ]
