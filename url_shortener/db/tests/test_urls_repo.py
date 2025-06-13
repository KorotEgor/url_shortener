import pytest
import tempfile
from pathlib import Path

from url_shortener.db.conn_to_db import init_db
from url_shortener.db.urls_repo import UrlsRepo


with open(Path(__file__).parent / "data.sql", "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def fake_db():
    _, db_path = tempfile.mkstemp()

    db = init_db(path=db_path)

    db.executescript(_data_sql)

    yield db

    db_path = Path(db_path)
    db_path.unlink()


async def test_get_short_by_user(fake_db):
    urls_repo = UrlsRepo(fake_db)

    short_url = await urls_repo.get_short_by_user("https://test")
    assert short_url == "http://localhost:8080/urls/test"


async def test_get_user_by_short(fake_db):
    urls_repo = UrlsRepo(fake_db)

    user_url = await urls_repo.get_user_by_short(
        "http://localhost:8080/urls/test"
    )
    assert user_url == "https://test"


async def test_compare_urls(fake_db):
    urls_repo = UrlsRepo(fake_db)

    is_good = await urls_repo.compare_urls(
        "https://test/test", "http://localhost:8080/urls/test2"
    )
    assert is_good

    assert fake_db.execute(
        "SELECT COUNT(*) FROM urls",
    ).fetchone() == (2,)
