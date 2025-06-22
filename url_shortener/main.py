from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging
import asyncio

from url_shortener.settings import BASE_DIR
from url_shortener.middlewares import setup_error_middleware
from url_shortener.views import Views
from url_shortener.db.conn_to_db import get_urls_repo, init_db
from url_shortener.utils.trans_url import TransUrl


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# app engine
async def main():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str(BASE_DIR / "url_shortener" / "templates")
        ),
    )

    con = await init_db()
    views = Views(urls_repo=get_urls_repo(con), tr_url=TransUrl())

    app.add_routes(
        [
            web.route("*", "/", views.home),
            web.get("/urls/{url}", views.urls),
            web.get("/bad_url", views.bad_url),
        ]
    )

    setup_error_middleware(app)

    runner = web.AppRunner(
        app,
        handle_signals=False,
    )
    await runner.setup()
    site = web.TCPSite(
        runner,
        "localhost",
        8080,
    )

    await site.start()

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        await runner.cleanup()
        await con.close()
        logger.info("Server stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("App stopped")
