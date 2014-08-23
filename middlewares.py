import json
import aiohttp.errors


class JsonMiddleware(object):

    def initialize_request(self, request):
        if request.method not in ("POST", "PUT"):
            return
        if request.headers.get('Content-Type', '') != 'application/json':
            raise aiohttp.errors.HttpException(415, 'Unsupported Media Type')
        try:
            request.data = json.loads(request.payload)
        except Exception:
            raise aiohttp.errors.HttpBadRequest()

    def finalize_response(self, request, response):
        response.data = bytearray(json.dumps(response.data), encoding='utf8')
        response.add_header('Content-Type', 'application/json')
        response.add_header('Content-Length', str(len(response.data)))
