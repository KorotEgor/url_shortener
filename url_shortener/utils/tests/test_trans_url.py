from url_shortener.utils.trans_url import TransUrl


async def test_get_short_url():
    tr_url = TransUrl()
    new_url1 = await tr_url.get_short_url()
    assert new_url1 == "http://localhost:8080/urls/b"

    new_url2 = await tr_url.get_short_url()
    assert new_url2 == "http://localhost:8080/urls/c"

    for i in range(2, 62):
        _ = await tr_url.get_short_url()

    new_url63 = await tr_url.get_short_url()
    assert new_url63 == "http://localhost:8080/urls/ab"
