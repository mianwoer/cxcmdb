import datetime
import time

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from cmdb import models
import django.contrib.auth as django_auth


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class IDCSerializer(ModelSerializer):
    class Meta:
        model = models.Idc
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class HostSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(HostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.Meta.depth = 1
        else:
            self.Meta.depth = 0

    class Meta:
        model = models.Host
        fields = '__all__'
        # depth = slef.M

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs

class IdcSerializer(ModelSerializer):
    class Meta:
        model = models.Idc
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = models.Cabinet
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class HostGroupSerializer(ModelSerializer):
    class Meta:
        model = models.HostGroup
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class InterFaceSerializer(ModelSerializer):
    class Meta:
        model = models.InterFace
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class IpSourceSerializer(ModelSerializer):
    class Meta:
        model = models.IpSource
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


class HostGroupSerializer(ModelSerializer):
    class Meta:
        model = models.HostGroup
        fields = '__all__'

    def validate(self, attrs):
        # attrs 是数据字典，包含request中post的数据
        return attrs


def time_diff(timestamp):
    onlineTime = datetime.datetime.fromtimestamp(timestamp)
    localTime = datetime.datetime.now()
    result = localTime - onlineTime
    hours = int(result.seconds / 3600)
    minutes = int(result.seconds % 3600 / 60)
    seconds = result.seconds % 3600 % 60
    if result.days > 0:
        x = f'{result.days}天前'
    elif hours > 0:
        x = f'{hours}小时前'
    elif minutes > 0:
        x = f'{minutes}分钟前'
    else:
        x = f'{seconds}秒前'
    return x


class SshTestSerializer(serializers.Serializer):
    host_ip = serializers.IPAddressField(required=True)
    ssh_port = serializers.IntegerField(default=22)
    os_user = serializers.CharField(required=True)
    os_passwd = serializers.CharField(required=True)

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_auth.models.User
        fields = ['username', 'password']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_auth.models.Group
        fields = '__all__'
        depth = 1


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_auth.models.Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """django用户模型序列化器，包含创建（注册）用户，查删改接口"""
    groups = serializers.PrimaryKeyRelatedField(queryset=django_auth.models.Group.objects.all(), required=False, many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=django_auth.models.Permission.objects.all(), required=False, many=True)

    class Meta:
        model = django_auth.models.User
        fields = '__all__'

    def create(self, validated_data):
        group_ids = validated_data.pop('groups', [])
        user_permissions_ids = validated_data.pop('user_permissions', [])
        if validated_data.get('is_superuser'):
            user = django_auth.models.User.objects.create_superuser(**validated_data)
        else:
            user = django_auth.models.User.objects.create_user(**validated_data)
        user.groups.set(group_ids)
        user.user_permissions.set(user_permissions_ids)
        return user

    def update(self, instance, validated_data):
        """更新用户信息,加密保存密码"""
        group_ids = validated_data.pop('groups', [])
        user_permissions_ids = validated_data.pop('user_permissions', [])
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if group_ids is not None:
            instance.groups.set(group_ids)
        if user_permissions_ids is not None:
            instance.user_permissions.set(user_permissions_ids)
        return instance
