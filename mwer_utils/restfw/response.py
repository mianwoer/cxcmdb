from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler as drf_exception_handler


class XRes(dict):
    def __init__(self, code, data=None, msg=None, **kwargs):
        super().__init__(**kwargs)
        self.code = self["code"] = code
        self.data = self["data"] = data
        self.msg = self["msg"] = msg or ""


def exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    >>> REST_FRAMEWORK = {
    ...     # ...
    ...     'EXCEPTION_HANDLER': 'sre_buff.utils.restfw.response.exception_handler',
    ...     # ...
    ... }
    For the parameters, see ``exception_handler``
    """
    res = drf_exception_handler(exc, context)
    if not res:
        return Response(
            data=str(exc), status=HTTP_500_INTERNAL_SERVER_ERROR, exception=True
        )
    return res
