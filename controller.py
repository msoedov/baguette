import asyncio


class ControllerType(type):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __new__(metacls, *args, **kwargs):
        cls = super().__new__(metacls, *args, **kwargs)
        for name in metacls.http_method_names:
            handler = getattr(cls, name, None)
            if handler and not asyncio.iscoroutinefunction(handler):
                raise ReferenceError('Method {}.{}.{} should be coroutine'.format(cls.__module__,
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