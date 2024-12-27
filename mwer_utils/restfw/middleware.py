"""
2021/2/3 14:38
django 中间件
"""
import json
import logging

from django.utils.deprecation import wareMixin
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from sre_buff.utils.django_util import validation_error_format
from sre_buff.utils.restfw.response import XRes

logger = logging.getLogger(__name__)


class ResponseSREMiddleware(MiddlewareMixin):
    # 201/204/400/500 请求默认HTTP_STATUS=200, 通过code == -1(内部报错) code=0(成功) code>1(可抛出异常msg)
    def process_response(self, request, response):
        if not hasattr(response, "accepted_media_type"):
            return response
        if response.accepted_media_type != "application/json":
            return response
        if response.status_code >= HTTP_500_INTERNAL_SERVER_ERROR:
            if response.data:
                response.content = json.dumps(dict(code=-1, msg=response.data))
                response["Content-Type"] = "application/json;charset=utf-8"
                response["Content-Length"] = len(response.content)
                response.status_code = HTTP_200_OK
                return response
            return response
        if response.status_code in [HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN]:
            return response
        if response.status_code in [HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT]:
            if not response.content:
                response.content = json.dumps(XRes(code=0, data=""))
            else:
                response.content = json.dumps(
                    XRes(code=0, data=json.loads(response.content))
                )
            response["Content-Type"] = "application/json;charset=utf-8"
            response["Content-Length"] = len(response.content)
            response.status_code = HTTP_200_OK
            return response
        if response.status_code == 400:
            response.content = json.dumps(
                XRes(**validation_error_format(response.data))
            )
            logger.error(
                "http_response: 400 http.method: %s http.path: %s http.res: %s"
                % (request.method, request.path, response.data)
            )
            response["Content-Type"] = "application/json;charset=utf-8"
            response["Content-Length"] = len(response.content)
            response.status_code = HTTP_200_OK
            return response
        return response
