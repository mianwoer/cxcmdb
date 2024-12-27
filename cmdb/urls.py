from django.urls import path, re_path, include
from cmdb import views as cmdbviews
from rest_framework import routers

router1 = routers.DefaultRouter()
# router2 = routers.DefaultRouter()
router1.register("host", cmdbviews.HostInfos)  # 主机信息
router1.register("project", cmdbviews.ProjectInfos)  # 项目信息
router1.register("idc", cmdbviews.IDCInfos)  # idc信息
router1.register("userInfo", cmdbviews.DjangoAuthUsers)  # 用户信息
router1.register("group", cmdbviews.DjangoAuthGroup)  # 组信息
router1.register("permission", cmdbviews.DjangoAuthPermission)  # 权限信息

urlpatterns = [
    re_path('', include(router1.urls)),
    re_path(r'sshtest/', cmdbviews.HostTestSsh.as_view()),  # 主机ssh连接测试
    re_path(r'getresource/', cmdbviews.UpdateHostInfoBySsh.as_view()),
    re_path(r'userSignin/', cmdbviews.DjangoAuthUserSingIn.as_view()),  # 用户登录
    re_path(r'userSignup/', cmdbviews.DjangoAuthUserSingUp.as_view()),  # 用户注册
    # re_path(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]
