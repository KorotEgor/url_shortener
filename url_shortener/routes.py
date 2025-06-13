from url_shortener.views import Views
from aiohttp import web


def setup_routes(app):
    views = Views()
    app.add_routes(
        [
            web.route("*", "/", views.home),
            web.get("/urls/{url}", views.urls),
            web.get("/bad_url", views.bad_url),
        ]
    )
