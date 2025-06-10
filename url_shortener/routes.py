from views import home
from aiohttp import web


def setup_routes(app):
    app.add_routes(
        [
            web.route("*", "/", home),
        ]
    )
