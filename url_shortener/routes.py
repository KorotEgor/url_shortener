from views import home_get, home_post
from aiohttp import web


def setup_routes(app):
    app.add_routes(
        [
            web.get("/", home_get),
            web.post("/", home_post),
        ]
    )
