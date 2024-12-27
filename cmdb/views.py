import json

import paramiko
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

import authControlApi
import django.contrib.auth as django_auth
from cmdb.serializers import *
from authControlApi.utils.auth import *
from rest_framework.exceptions import ValidationError

from cmdb import models
from mwer_utils import crud
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data_, msg="success", code=200):
    data = {
        "code": code,
        "msg": msg,
        "data": data_,
    }
    return response_as_json(data)


class HostInfos(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = HostSerializer
    # pagination_class = None
    queryset = models.Host.objects.all()


class ProjectInfos(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectSerializer
    # pagination_class = None
    queryset = models.Project.objects.all()
    # permission_classes = [IsAuthenticated,]


class IDCInfos(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = IDCSerializer
    # pagination_class = None
    queryset = models.Idc.objects.all()


class HostTestSsh(GenericAPIView):
    """根据主机的密码尝试建立ssh连接，验证是否成功"""
    serializer_class = SshTestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        HostTest_ssh = paramiko.SSHClient()
        HostTest_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            HostTest_ssh.connect(serializer.data.get("host_ip"), serializer.data.get("ssh_port"),
                                 serializer.data.get("os_user"), serializer.data.get("os_passwd"), timeout=5)
            return json_response("ssh测试通过")
        except Exception as e:
            return json_response(None, msg=str(e), code=444)
        finally:
            HostTest_ssh.close()


# ssh登录redhat系 linux系统后获取设备部分信息
def get_resource(host, user, passwd, fileSystem='/$', port=22):
    """建立ssh远程连接，获取某台linux设备的基础信息"""
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_.connect(host, port, user, passwd, timeout=5)
        stdin1, cpu, stderr1 = \
            ssh_.exec_command(''' export LANG=en_US.UTF-8;lscpu |egrep '^CPU\(s\)'|awk 'BEGIN{ORS=""} {print $2}' ''',
                              timeout=3)
        stdin2, memory, stderr2 = \
            ssh_.exec_command(''' export LANG=en_US.UTF-8;free -g | grep 'Mem' | awk 'BEGIN{ORS=""} {print $2}' ''',
                              timeout=3)
        stdin3, disk, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;lsblk -d | awk 'NR > 2,ORS="," {print prev1,prev2}{prev1=$1}{prev2=$4}END{printf"%s %s" ,$1,$4}' ''',
                timeout=3)
        stdin3, sn, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;dmidecode -t system | grep Serial| awk -F": " 'BEGIN{ORS=""}{print $2}' ''',
                timeout=3)
        stdin3, cpu_model, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;lscpu|grep "Model name"|awk '{ORS=""}{print substr($0, index($0, $3))}' ''',
                timeout=3)

        resource_dict = {'ip': host,
                         'cpus': str(cpu.read().decode('utf-8')),
                         'memory': str(int(memory.read().decode('utf-8'))) + 'g',
                         'disk': str(disk.read().decode('utf-8')),
                         'sn': str(sn.read().decode('utf-8')),
                         'cpu_model': str(cpu_model.read().decode('utf-8'))}
    except Exception as e:
        # return {"result": "1",  # 代表失败
        #         "data": e}
        raise e
    finally:
        ssh_.close()
    # print(resource_dict)
    return {"result": 0,  # 代表成功
            "data": resource_dict}


# ssh登录ubuntu系 linux系统后获取设备部分信息,待实现
class UpdateHostInfoBySsh(GenericAPIView):
    """get请求，获取全量、“使用中”状态的系统设备的设备信息"""
    serializer_class = HostSerializer

    def get(self, request, *args, **kwargs):
        # 如果操作系统是linux，且系统有用户名，密码。则通过ssh登录上去获取部分信息
        # 分类系统，centos、ubuntu
        queryset = models.Host.objects.all().filter(status=1)  # 获取使用中的设备
        serializer = self.get_serializer(queryset, many=True)  # 将设备反序列化成对象
        api_return = {}
        for _host in serializer.data:
            try:
                _pk = _host.get("id")
                _host_ip = _host.get("ip")
                _host_os_user = _host.get("os_user")
                _host_os_passwd = _host.get("os_passwd")
                _host_para = get_resource(_host_ip, _host_os_user, _host_os_passwd)
                if _host_para.get("result") == 0:  # 判断ssh执行返回成功
                    cpu_num = _host_para.get("data").get("cpus")
                    memory = _host_para.get("data").get("memory")
                    disk = _host_para.get("data").get("disk")
                    sn = _host_para.get("data").get("sn")
                    cpu_model = _host_para.get("data").get("cpu_model")
                    _crud = crud.Exsql()
                    _sql = ''' update cmdb_host set cpu_num=%s,memory=%s,disk=%s,sn=%s,cpu_model=%s where id=%s '''
                    result = _crud.update(_sql, cpu_num, memory, disk, sn, cpu_model, _pk)
                    api_return[_host_ip] = "获取配置参数成功，更新%s条记录" % result
            except Exception as e:  # ssh或者sql执行异常
                api_return[_host_ip] = str(e)
            # return json_response({"affected_rows_count": }, msg=str(e), code=400)
        return json_response(api_return)  # 更新数据量


class DjangoAuthUsers(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """用户信息表视图，去掉post（create）请求"""
    description = "这是一个系统用户数据视图，用于查、改用户信息。需要进行用户认证、权限"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = None
    queryset = django_auth.models.User.objects.all()

class DjangoAuthUserSingUp(CreateAPIView):
    """用户注册接口"""
    description = "这是一个系统用户数据视图，用于新增（注册）用户信息，不需要认证"
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer
    pagination_class = None
    queryset = django_auth.models.User.objects.all()

class DjangoAuthUserSingIn(GenericAPIView):
    """用户登录接口"""
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = django_auth.authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return json_response({'token': token.key})
        # return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return json_response('error', msg="用户不存在", code=400)


class DjangoAuthGroup(ModelViewSet):
    description = "Auth模块的Group表视图"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    # pagination_class = None
    queryset = django_auth.models.Group.objects.all()


class DjangoAuthPermission(ModelViewSet):
    description = "Auth模块的Permission表视图"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer
    # pagination_class = None
    queryset = django_auth.models.Permission.objects.all()
