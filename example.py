import asyncio
from app import App
from controller import Controller
from generics import JsonAPI
from errors import ApiError
from middlewares import LoggerMiddleware, BasicAuthMiddleware


class Example(JsonAPI):

    @asyncio.coroutine
    def get(self, context):
        return {}


class Hello(JsonAPI):

    @asyncio.coroutine
    def get(self, context):
        return 'Hello'


class Bye(JsonAPI):

    @asyncio.coroutine
    def get(self, context):
        return 'Bye'


app = App()

# app.use(AuthMiddleware, NewrelicMiddleware, SentryMiddleware)

# db = NewDatabasePool()
# app.map(db)

#
app.group('/v1/api',
          ('/hello/', Hello),
          ('/bye', Bye.params(foo='bar'))
          ).use(LoggerMiddleware())

app.group('/',
          ('', Example)
          ).use(LoggerMiddleware(), BasicAuthMiddleware({'admin': 'admin'}))

# app.group('/v1/api',
#           ('/hello/{name}', lambda: ""),
#           ('/hello/{name}', lambda: "")
#           ).use(JsonMiddleware())

app.run()