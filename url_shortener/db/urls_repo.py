import logging
from sqlite3 import DatabaseError

logger = logging.getLogger(__name__)


class UrlsRepo:
    def __init__(self, db):
        self.db = db

    async def compare_urls(self, user_url, short_url):
        try:
            self.db.execute(
                "INSERT INTO urls (user_url, short_url) VALUES (?, ?)",
                (user_url, short_url),
            )
            self.db.commit()
        except DatabaseError as err:
            logger.error(f"Error while comparing urls: {err}")
            return False

        logger.info(f"Added new line to urls table: {user_url} -> {short_url}")
        return True

    async def get_user_by_short(self, short_url):
        try:
            cur = self.db.execute(
                "SELECT user_url FROM urls WHERE short_url = ?",
                (short_url,),
            )
            user_url = cur.fetchone()
        except DatabaseError as err:
            logger.error(f"Error while getting user_url by short_url: {err}")
            return None

        if user_url is not None:
            user_url = user_url[0]
            logger.info(f"Found user_url {user_url} by short_url {short_url}")

        return user_url

    async def get_short_by_user(self, user_url):
        try:
            cur = self.db.execute(
                "SELECT short_url FROM urls WHERE user_url = ?",
                (user_url,),
            )
            short_url = cur.fetchone()
        except DatabaseError as err:
            logger.error(f"Error while getting short_url by user_url: {err}")
            return None

        if short_url is not None:
            short_url = short_url[0]
            logger.info(f"Found short_url {short_url} by user_url {user_url}")

        return short_url
