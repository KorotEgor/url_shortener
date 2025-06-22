import aiosqlite
import logging

from url_shortener.db.urls_repo import UrlsRepo

logger = logging.getLogger(__name__)


async def init_db(path="url_shortener.db"):
    con = await aiosqlite.connect(path)

    with open("url_shortener/db/schema.sql", "rb") as f:
        await con.executescript(f.read().decode("utf8"))
    logger.info("Database initialized")

    return con


def get_urls_repo(con):
    return UrlsRepo(con)
