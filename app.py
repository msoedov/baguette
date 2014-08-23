import aiohttp.server

import asyncio
from urllib.parse import urlparse, parse_qsl
from aiohttp.multidict import MultiDict
from operator import methodcaller
from itertools import dropwhile
from group import Group


class App(object):

    def __init__(self):
        self.global_mw = []
        self.groups = []

    def use(self, *mw):
        """
        :param mw:
        :return:
        """

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
            h, *_ = dropwhile(lambda x: x.regexp.match(request.method) is None, handlers)
            return h

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

    def __init__(self, dispatcher=None, **kwargs):
        self.dispatcher = dispatcher
        super().__init__(**kwargs)

    @asyncio.coroutine
    def handle_request(self, request, payload):
        response = aiohttp.Response(self.writer, 200, http_version=request.version)

        handler = self.dispatcher(request)
        request.payload = lambda *a: (yield from payload.read())
        request.query = MultiDict(parse_qsl(urlparse(request.path).query))
        handler.initialize_request(request)
        results = yield from getattr(handler, request.method.lower())(request)
        response.data = results
        handler.finalize_response(request, response)
        response.send_headers()
        response.write(response.data)
        yield from response.write_eof()
