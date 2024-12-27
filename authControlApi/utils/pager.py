from rest_framework import serializers
from authControlApi import models


class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
