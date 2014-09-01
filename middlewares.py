import logging
import time
import base64
from errors import ApiError

logger = logging.getLogger()


class LoggerMiddleware(object):
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def initialize_request(self, context):
        self.st = time.time()

    def finalize_response(self, context):
        dt = time.time() - self.st
        dt *= 1000
        request, response = context.request, context.response
        collor = self.OKGREEN if response.status < 400 else self.FAIL
        logger.warn('{} {} {}|{}|{} completed in {:1.2f}ms'.format(request.method,
                                                                   request.path,
                                                                   collor,
                                                                   response.status,
                                                                   self.ENDC,
                                                                   dt))


class BasicAuthMiddleware(object):
    realm = 'basic-auth'

    def __init__(self, auth_source):
        self.auth_source = auth_source

    def initialize_request(self, context):
        request = context.request
        val = request.headers.get('AUTHORIZATION', '')
        if not val:
            return self.fail('Auth required')
        auth_method, creds = val.split(' ')
        if auth_method.lower() != 'basic':
            return self.fail('Bad auth method')
        try:
            auth_parts = base64.b64decode(creds).decode('utf-8').partition(':')
        except (TypeError, UnicodeDecodeError):
            return self.fail('Invalid auth header')
        username, password = auth_parts[0], auth_parts[2]
        if self.auth_source.get(username) != password:
            return self.fail('Invalid credential')

    def fail(self, msg):
        raise ApiError(401, msg)

    def finalize_response(self, context):
        """
        """
