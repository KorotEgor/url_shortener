import pytest
from aiohttp import web
import aiohttp_jinja2
import jinja2
from url_shortener.settings import BASE_DIR
from unittest.mock import AsyncMock


from url_shortener.views import Views


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
        "http://localhost:8080/urls/short_url",
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
        ]
    )
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str(BASE_DIR / "url_shortener" / "tests" / "fixtures")
        ),
    )
    return await aiohttp_client(app)


async def test_home(cli):
    resp = await cli.get("/")
    assert resp.status == 200

    resp = await cli.post("/", data={"user_url": "bad_url"})
    assert resp.status == 200
    with open("url_shortener/tests/fixtures/home_bad_url.html", "rb") as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/user_url"}
    )
    assert resp.status == 200
    with open("url_shortener/tests/fixtures/home_url_created.html", "rb") as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/user_url"}
    )
    assert resp.status == 200
    with open("url_shortener/tests/fixtures/home_error.html", "rb") as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/another_user_url"}
    )
    assert resp.status == 200
    with open("url_shortener/tests/fixtures/home_url_created.html", "rb") as f:
        text = await resp.read()
        print(text.decode("utf8"))
        assert text == f.read()
