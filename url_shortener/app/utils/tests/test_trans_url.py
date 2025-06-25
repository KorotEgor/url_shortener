from url_shortener.app.utils.trans_url import TransUrl, get_last_coomb
from unittest.mock import AsyncMock


async def test_get_short_url_empty():
    tr_url = TransUrl()
    new_url1 = await tr_url.get_short_url()
    assert new_url1 == "http://localhost:8080/urls/b"

    new_url2 = await tr_url.get_short_url()
    assert new_url2 == "http://localhost:8080/urls/c"

    for i in range(2, 62):
        _ = await tr_url.get_short_url()

    new_url63 = await tr_url.get_short_url()
    assert new_url63 == "http://localhost:8080/urls/ab"


async def test_get_short_url_data():
    tr_url = TransUrl("c")

    assert tr_url.last_coomb == "http://localhost:8080/urls/"
    assert tr_url.last_ch_num == 3
    assert tr_url.last_added_ch_num == 0

    tr_url = TransUrl("cc")

    assert tr_url.last_coomb == "http://localhost:8080/urls/c"
    assert tr_url.last_ch_num == 3
    assert tr_url.last_added_ch_num == 2


async def test_get_last_coomb():
    urls_repo = AsyncMock()

    urls_repo.get_last_short_url.side_effect = [
        "http://localhost:8080/urls/test",
        None,
    ]

    last_coomb1 = await get_last_coomb(urls_repo)
    assert last_coomb1 == "test"

    last_coomb2 = await get_last_coomb(urls_repo)
    assert last_coomb2 == ""
