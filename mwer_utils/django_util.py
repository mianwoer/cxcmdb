import datetime

import pytz
from django.conf import settings
from django.forms.models import model_to_dict
from rest_framework.utils.serializer_helpers import ReturnDict


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


local_tz = pytz.timezone(settings.TIME_ZONE)


def utc_to_local(utc_dt):
    """将UTC时区转化为local时区"""
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def _error_code(value):
    if value == "blank":
        return 1
    if value == "required":
        return 1
    if value == "invalid":
        return 1
    elif value == "null":
        return 1
    elif value == "max_length":
        return 1
    elif value == "invalid_choice":
        return 1
    elif value == "incorrect_type":
        return 1
    elif value == "unique":
        return 1
    else:
        return int(value)


def validation_error_format(edetail):
    """将validation error 转化为dict"""
    if isinstance(edetail, ReturnDict):
        for key, value in edetail.items():
            if not hasattr(value[0], "code"):
                # 兼容嵌套Serializer
                for key_sub, value_sub in value[0].items():
                    return dict(
                        msg="{}-{}:{}".format(key, key_sub, str(value_sub[0])),
                        code=_error_code(getattr(value_sub[0], "code")),
                    )
            return dict(
                msg="{}:{}".format(key, str(value[0])),
                code=_error_code(getattr(value[0], "code")),
            )
    return dict(msg="", code=1)


def model_to_dict_restfw(instance, fields=None, exclude=None):
    data = model_to_dict(instance, fields, exclude)
    for key, value in data.items():
        if value is None:
            data[key] = ""
    return data


def local_to_utc(local_tz, dt_1, dt_2):
    """
    local_tz : any possible timezone which supports pytz lib (https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones)
    dt_1 and dt_2 : local datetime in string in this format ->> '%Y-%m-%dT%H:%M:%S'

    return a list as ->> [utc_equivalent_of_dt_1_in_string,utc_equivalent_of_dt_2_in_string]
    """
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    pytz_local_tz = pytz.timezone(local_tz)
    dt_obj_from_date_time = datetime.datetime.strptime(dt_1, format)
    dt_obj_to_date_time = datetime.datetime.strptime(dt_2, format)
    return [
        pytz_local_tz.localize(dt_obj_from_date_time)
        .astimezone(tz=pytz.utc)
        .strftime(format),
        pytz_local_tz.localize(dt_obj_to_date_time)
        .astimezone(tz=pytz.utc)
        .strftime(format),
    ]
