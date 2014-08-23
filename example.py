import asyncio
from app import App
from controller import Controller


class Example(Controller):

    @asyncio.coroutine
    def get(self, request, **kw):
        json = request.data
        return {}

app = App()

# app.use(AuthMiddleware, NewrelicMiddleware, SentryMiddleware)

# db = NewDatabasePool()
# app.map(db)


# app.group('/v1/api',
#           ('GET', '/hello/{name}', say_hello),
#           ('POST', '/hello/{name}', say_hello)
#         ).use(CorsMiddlevare)#

app.group('/v1/api',
          ('/hello/{name}', lambda: ""),
          ('/hello/{name}', lambda: "")
          )

app.run()