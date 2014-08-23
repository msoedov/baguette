import asyncio
from app import App
from controller import Controller
from middlewares import JsonMiddleware


class Example(Controller):

    @asyncio.coroutine
    def get(self, request, **kw):
        return {}

app = App()

# app.use(AuthMiddleware, NewrelicMiddleware, SentryMiddleware)

# db = NewDatabasePool()
# app.map(db)


# app.group('/v1/api',
#           ('GET', '/hello/{name}', say_hello),
#           ('POST', '/hello/{name}', say_hello)
#         ).use(CorsMiddlevare)#

app.group('/',
          ('', Example)
          ).use(JsonMiddleware())

# app.group('/v1/api',
#           ('/hello/{name}', lambda: ""),
#           ('/hello/{name}', lambda: "")
#           ).use(JsonMiddleware())

app.run()