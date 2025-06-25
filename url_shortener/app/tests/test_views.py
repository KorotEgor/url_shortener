from url_shortener.app.tests.fake_client import cli  # noqa: F401


async def test_home(cli):  # noqa: F811
    resp = await cli.get("/")
    assert resp.status == 200

    resp = await cli.post("/", data={"user_url": "bad_url"})
    assert resp.status == 200
    with open(
        "url_shortener/app/tests/fixtures/home_pages/home_bad_url.html", "rb"
    ) as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/user_url"}
    )
    assert resp.status == 200
    with open(
        "url_shortener/app/tests/fixtures/home_pages/home_url_created.html",
        "rb",
    ) as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/user_url"}
    )
    assert resp.status == 200
    with open(
        "url_shortener/app/tests/fixtures/home_pages/home_error.html", "rb"
    ) as f:
        text = await resp.read()
        assert text == f.read()

    resp = await cli.post(
        "/", data={"user_url": "http://localhost:8080/user_url"}
    )
    assert resp.status == 200
    with open(
        "url_shortener/app/tests/fixtures/home_pages/home_url_created.html",
        "rb",
    ) as f:
        text = await resp.read()
        assert text == f.read()


async def test_bad_url(cli):  # noqa: F811
    resp = await cli.get("/bad_url")
    assert resp.status == 200
    with open(
        "url_shortener/app/tests/fixtures/error_pages/bad_url_resp.html", "rb"
    ) as f:
        text = await resp.read()
        assert text == f.read()
