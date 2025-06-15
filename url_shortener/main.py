from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging


from url_shortener.settings import BASE_DIR
from url_shortener.middlewares import setup_error_middleware
from url_shortener.views import Views
from url_shortener.db.conn_to_db import get_urls_repo
from url_shortener.utils.trans_url import TransUrl


logging.basicConfig(level=logging.INFO)

# app engine
# Лучше сделать функцию
def run():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str(BASE_DIR / "url_shortener" / "templates")
        ),
    )

    views = Views(urls_repo=get_urls_repo(), tr_url=TransUrl())

    app.add_routes(
        [
            web.route("*", "/", views.home),
            web.get("/urls/{url}", views.urls),
            web.get("/bad_url", views.bad_url),
        ]
    )

    setup_error_middleware(app)

    web.run_app(app)

if __name__ == "__main__":
    run()
