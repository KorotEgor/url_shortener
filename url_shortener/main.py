from aiohttp import web
import aiohttp_jinja2
import jinja2
import logging


from url_shortener.routes import setup_routes
from settings import BASE_DIR
from url_shortener.middlewares import setup_error_middleware


logging.basicConfig(level=logging.INFO)

# app engine
app = web.Application()
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(
        str(BASE_DIR / "url_shortener" / "templates")
    ),
)
setup_routes(app)
setup_error_middleware(app)

if __name__ == "__main__":
    web.run_app(app)
