import errors
from controller import Controller
from parsers import JSONParser


class JsonAPI(Controller):

    def initialize_request(self, request):
        if request.method not in ("POST", "PUT"):
            return
        if request.headers.get('Content-Type', '') != 'application/json':
            raise errors.ApiError(415, '')
        try:
            request.data = JSONParser.parse(request.payload)
        except Exception as e:
            raise errors.ApiError(400, str(e))

    def finalize_response(self, request, response):
        response.data = JSONParser.render(response.data)
        response.add_header('Content-Type', 'application/json')
        response.add_header('Content-Length', str(len(response.data)))