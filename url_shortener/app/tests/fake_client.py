import pytest
from aiohttp import web
import aiohttp_jinja2
import jinja2
from url_shortener.settings import BASE_DIR
from unittest.mock import AsyncMock


from url_shortener.app.views import Views
from url_shortener.app.middlewares import setup_error_middleware


async def err_handler(request):
    raise web.HTTPException("test")


@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()

    urls_repo = AsyncMock()

    urls_repo.get_short_by_user.side_effect = [
        "http://localhost:8080/urls/short_url",
        None,
        None,
    ]
    urls_repo.compare_urls.side_effect = [False, True]

    urls_repo.get_user_by_short.side_effect = [
        "http://localhost:8080/",
        None,
    ]

    tr_url = AsyncMock()
    tr_url.get_short_url.return_value = "http://localhost:8080/urls/short_url"

    views = Views(urls_repo=urls_repo, tr_url=tr_url)
    app.add_routes(
        [
            web.route("*", "/", views.home),
            web.get("/urls/{url}", views.urls),
            web.get("/bad_url", views.bad_url),
            web.get("/err_handle", err_handler),
        ]
    )

    setup_error_middleware(app)

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str(BASE_DIR / "url_shortener" / "app" / "tests" / "fixtures")
        ),
    )
    return await aiohttp_client(app)
