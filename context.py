import asyncio
from urllib.parse import urlparse, parse_qsl
from aiohttp.multidict import MultiDict
from aiohttp.protocol import Response as R

UNEVALUATED = object()


class Context(object):

    def __init__(self, request, response, payload):
        self.request = request
        self.response = response
        self.payload = payload
        self.query = MultiDict(parse_qsl(urlparse(request.path).query))
        self._content = UNEVALUATED

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        if self._content is UNEVALUATED:
            self._content = val
        else:
            raise ValueError('Already exist')

    def apply(self, fn):
        self._content = fn(self.content)

    @asyncio.coroutine
    @property
    def data(self):
        return (yield from self.payload.read())

    def __getattr__(self, attr):
        return self.__dict__.get(attr, None)

    @asyncio.coroutine
    def write(self):
        self.response.add_header('Content-Length', str(len(self._content)))
        self.response.write(self._content)
        yield from self.response.write_eof()


class Response(R):
    SERVER_SOFTWARE = 'PHP5.1:)'
    _send_headers = True
