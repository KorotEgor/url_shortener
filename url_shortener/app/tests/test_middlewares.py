from url_shortener.app.tests.fake_client import cli  # noqa: F401


async def test_404(cli):  # noqa: F811
    resp = await cli.get("/test")
    assert resp.status == 404

    with open(
        "url_shortener/app/tests/fixtures/error_pages/404.html", "rb"
    ) as f:
        text = await resp.read()
        assert text == f.read()


async def test_500(cli):  # noqa: F811
    resp = await cli.get("/err_handle")
    assert resp.status == 500

    with open(
        "url_shortener/app/tests/fixtures/error_pages/500.html", "rb"
    ) as f:
        text = await resp.read()
        assert text == f.read()
