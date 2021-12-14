
from django.http import JsonResponse


class Response:
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class Error(Response):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class Success(Response):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)



def validData(success_config: Success, error_config: Error, valid=True):
    def inner(func):
        def isValid(cls, request, *args, **kwargs):
            import copy
            # 深拷贝，防止损坏原字典
            ret = copy.deepcopy(success_config.__dict__)
            try:
                # 断言，判断是否存在字段为空情况
                if valid:
                    assert \
                    len([value for value in (request.data or request.query_params)
                       .keys() if value]) == \
                    len([value for value in (request.data or request.query_params)
                        .values() if value]), '参数不足'

                # 要求返回 data 域数据，而非 Response
                data = func(cls, request, *args, **kwargs)
                if data: ret['data'] = data
            except Exception as e:
                ret.update(error_config.__dict__)
                ret['error'] = str(e)
            return JsonResponse(ret)
        return isValid
    return inner
