import json
import aiohttp.errors


class JsonMiddleware(object):

    def initialize_request(self, request):
        if request.headers.get('Content-Type', '') != 'application/json':
            raise aiohttp.errors.HttpException(415, 'Unsupported Media Type')
        try:
            request.data = json.loads(request.payload)
        except Exception:
            raise aiohttp.errors.HttpBadRequest()

    def finalize_response(self, request, response):
        response.data = json.dumps(response.data)
        response.add_header('Content-Type', 'application/json')
        response.add_header('Content-Length', len(response.data))
