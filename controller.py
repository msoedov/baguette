import asyncio
from errors import ApiError


class ControllerType(type):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __new__(metacls, *args, **kwargs):
        cls = super().__new__(metacls, *args, **kwargs)
        cls.allowed_methods = []
        for name in metacls.http_method_names:
            handler = getattr(cls, name, None)
            if handler:
                cls.allowed_methods.append(name)
                if not asyncio.iscoroutinefunction(handler):
                    raise TypeError('Method {}.{}.{} should be coroutine'.format(cls.__module__,
                                                                                 cls.__name__,
                                                                                 name))
        return cls


class Controller(object, metaclass=ControllerType):

    def initialize_request(self, request):
        """

        :param request:
        :return:
        """

    def finalize_response(self, request, response):
        """
        :param request:
        :param response:
        :return:
        """

    def not_allowed(cls, *a):
        raise ApiError(405, {'allowed methods': cls.allowed_methods})
