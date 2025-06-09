from views import home


def setup_routes(app):
    app.router.add_get("/", home)
