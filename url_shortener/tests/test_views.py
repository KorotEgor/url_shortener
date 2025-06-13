import pytest
from aiohttp import web

from url_shortener.views import home, urls, bad_url


@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()
    app.add_routes(
        [
            web.route("*", "/", home),
            web.get("/urls/{url}", urls),
            web.get("/bad_url", bad_url),
        ]
    )
    return await aiohttp_client(app)
