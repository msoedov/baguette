from app import App

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