import sqlite3
import logging

logger = logging.getLogger(__name__)


def init_db():
    con = sqlite3.connect("url_shortener.db")

    with open("url_shortener/db/schema.sql", "rb") as f:
        con.executescript(f.read().decode("utf8"))
    logger.info("Database initialized")

    return con
