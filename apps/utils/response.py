# 状态码
class ReturnCode:
    SUCCESS = 1000

    FAILED = -100
    WRONG_PARMAS = -101
    RESOURCE_NOT_FOUND = -102

    UNAUTHORIZED = -500
    BROKEN_AUTHORIZED_DATA = -501
    SESSION_EXPIRED = -502

    @classmethod
    def message(cls, code):
        if code == cls.SUCCESS:
            return 'success'
        elif code == cls.FAILED:
            return 'failed'
        elif code == cls.UNAUTHORIZED:
            return 'unauthorized'
        elif code == cls.WRONG_PARMAS:
            return 'wrong params'
        elif code == cls.RESOURCE_NOT_FOUND:
            return 'resources not found'
        elif code == cls.UNAUTHORIZED:
            return 'request unauthorized'
        elif code == cls.BROKEN_AUTHORIZED_DATA:
            return 'broken authorized data'
        elif code == cls.SESSION_EXPIRED:
            return 'session expired'


class CommonResponseMixin(object):
    @classmethod
    def wrap_json_response(cls, data=None, code=None, message=None, count=None, filename=None):
        response = {}
        res_data = []
        if not code:
            code = ReturnCode.SUCCESS
        if not message:
            message = ReturnCode.message(code)
        if data:
            res_data = data
            response['count'] = count
        if filename:
            response['file_url'] = filename
        response['data'] = res_data
        response['error_code'] = code
        response['message'] = message

        return response
