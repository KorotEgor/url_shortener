from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging
import asyncio

from url_shortener.settings import BASE_DIR
from url_shortener.middlewares import setup_error_middleware
from url_shortener.views import Views
from url_shortener.db.conn_to_db import get_urls_repo, init_db
from url_shortener.utils.trans_url import TransUrl, get_last_coomb


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# app engine
async def get_app_and_con():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str(BASE_DIR / "url_shortener" / "templates")
        ),
    )

    con = await init_db()
    urls_repo = get_urls_repo(con)
    tr_url = TransUrl(await get_last_coomb(urls_repo))
    views = Views(urls_repo=urls_repo, tr_url=tr_url)

    app.add_routes(
        [
            web.route("*", "/", views.home),
            web.get("/urls/{url}", views.urls),
            web.get("/bad_url", views.bad_url),
        ]
    )

    setup_error_middleware(app)

    return app, con


def run():
    app, con = asyncio.run(get_app_and_con())
    web.run_app(app)
    asyncio.run(con.close())


if __name__ == "__main__":
    run()
