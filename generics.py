import errors
from controller import Controller
from parsers import JSONParser


class JsonAPI(Controller):

    def initialize_request(self, context):
        request = context.request
        if request.method not in ("POST", "PUT"):
            return
        if request.headers.get('Content-Type', '') != 'application/json':
            raise errors.ApiError(415, '')
        try:
            request.data = JSONParser.parse(request.payload)
        except Exception as e:
            raise errors.ApiError(400, str(e))

    def finalize_response(self, context):
        context.apply(JSONParser.render)
        context.response.add_header('Content-Type', 'application/json')
