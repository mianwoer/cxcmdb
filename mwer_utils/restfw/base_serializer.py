# -*- encoding: utf-8 -*-
"""
@File    :   base_serializer.py
@Time    :   2021/03/02 16:01:44
@Author  :   krypln
@Version :   1.0
@Contact :   yiyito@yeah.com
"""

# here put the import lib

from rest_framework import serializers


class BaseSerializers(serializers.ModelSerializer):
    """
    时间处理，两中方法
    """

    # id = serializers.IntegerField(required=False)  # 只序列化，不走校验
    create_time = serializers.SerializerMethodField()
    update_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", required=False, read_only=True
    )

    def get_create_time(self, obj):
        """
        # 函数名为 get_ + 自定义的字段名 => get_create_time
        :param obj:
        :return:
        """
        return obj.create_time.strftime("%Y-%m-%d %H:%M")
