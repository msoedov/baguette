import asyncio
from app import App
from controller import Controller
from generics import JsonAPI
from errors import ApiError
from middlewares import LoggerMiddleware, BasicAuthMiddleware


class Example(JsonAPI):

    @asyncio.coroutine
    def get(self, request, **kw):
        return {}

app = App()

# app.use(AuthMiddleware, NewrelicMiddleware, SentryMiddleware)

# db = NewDatabasePool()
# app.map(db)

#
# app.group('/v1/api',
#           ('GET', '/hello/{name}', say_hello),
#           ('POST', '/hello/{name}', say_hello)
#           ).use(JsonAPI)

app.group('/',
          ('', Example)
          ).use(LoggerMiddleware(), BasicAuthMiddleware({'admin': 'admin'}))

# app.group('/v1/api',
#           ('/hello/{name}', lambda: ""),
#           ('/hello/{name}', lambda: "")
#           ).use(JsonMiddleware())

app.run()