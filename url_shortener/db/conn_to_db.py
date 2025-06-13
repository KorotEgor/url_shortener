import sqlite3
import logging

from url_shortener.db.urls_repo import UrlsRepo

logger = logging.getLogger(__name__)


def init_db(path="url_shortener.db"):
    con = sqlite3.connect(path)

    with open("url_shortener/db/schema.sql", "rb") as f:
        con.executescript(f.read().decode("utf8"))
    logger.info("Database initialized")

    return con


def get_urls_repo():
    return UrlsRepo(init_db())
