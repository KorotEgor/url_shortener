from url_shortener.db.conn_to_db import get_urls_repo
from url_shortener.db.urls_repo import UrlsRepo


async def test_get_urls_repo():
    assert isinstance(get_urls_repo("test"), UrlsRepo)
