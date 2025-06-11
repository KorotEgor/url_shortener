from views import home, urls, bad_url
from aiohttp import web


def setup_routes(app):
    app.add_routes(
        [
            web.route("*", "/", home),
            web.get("/urls/{url}", urls),
            web.get("/bad_url", bad_url),
        ]
    )
