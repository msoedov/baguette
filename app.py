import asyncio
import aiohttp.server

from urllib.parse import urlparse, parse_qsl
from aiohttp.multidict import MultiDict
from operator import methodcaller
from itertools import dropwhile
from group import Group, EmptyRoute
from parsers import JSONParser
from errors import ApiError
import logging

loger = logging.getLogger(__name__)


class App(object):

    def __init__(self):
        self.global_mw = []
        self.groups = []

    def use(self, *mw):
        """
        :param mw:
        :return:
        """
        self.global_mw.extend(mw)

    def group(self, *_):
        """

        :param path:
        :param rules:
        :return:
        """
        group = Group(*_)
        self.groups.append(group)
        return group

    def map(self, parameter):
        """

        :param parameter:
        :return:
        """

    def run(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        handlers = sum(map(methodcaller('as_handlers'), self.groups), [])
        handlers = [h.compile() for h in handlers]

        def dispatcher(request):
            for handler in handlers:
                if handler.regexp.match(request.path) is not None:
                    return handler
            raise ApiError(404, 'Not found')

        @asyncio.coroutine
        def serve(host="0.0.0.0", port=8080, **kwargs):
            return (yield from asyncio.get_event_loop().create_server(lambda: HttpRequestHandler(dispatcher),
                                                                                                 host,
                                                                                                 port,
                                                                                                 **kwargs))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serve())
        loop.run_forever()


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
    default_renderer = JSONParser
    route = EmptyRoute

    def __init__(self, dispatcher=None, **kwargs):
        self.dispatcher = dispatcher
        super().__init__(**kwargs)

    @asyncio.coroutine
    def handle_request(self, request, payload):
        response = aiohttp.Response(self.writer, 200, http_version=request.version)

        self.route = self.dispatcher(request)
        handler = self.route.fn()
        if request.method in ("POST", "PUT"):
            request.payload = yield from payload.read()
        # request.query = MultiDict(parse_qsl(urlparse(request.path).query))
        [u.initialize_request(request) for u in self.route.uses]
        handler.initialize_request(request)
        results = yield from getattr(handler, request.method.lower(), handler.not_allowed)(request)
        response.data = results
        handler.finalize_response(request, response)
        [u.finalize_response(request, response) for u in self.route.uses]
        response.send_headers()
        response.write(response.data)
        yield from response.write_eof()

    def handle_error(self, status=500, message=None, payload=None, exc=None, headers=None):
        try:
            if isinstance(exc, ApiError):
                details = exc.message
                status = exc.code
            else:
                details = 'Something went wrong'
                status = 500
                loger.exception(details)
            r = aiohttp.Response(self.writer, status, close=True)
            details = self.default_renderer.render({'message': details,
                                                    'path': message.path,
                                                    'method': message.method})
            r.add_header('Content-Type', self.default_renderer.media_type)
            r.add_header('Content-Length', '%s' % len(details))
            r.send_headers()
            r.write(details)
            [u.finalize_response(message, r) for u in self.route.uses]
            r.write_eof()
            self.keep_alive(False)
        except Exception as e:
            loger.exception('')
