from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import logging

from url_shortener.db.scheme import Urls

logger = logging.getLogger(__name__)


class UrlsRepo:
    def __init__(self, engine):
        self.engine = engine

    async def compare_urls(self, user_url, short_url):
        with Session(self.engine) as session:
            new_line = Urls(
                user_url=user_url,
                short_url=short_url,
            )

            try:
                session.add(new_line)
            except SQLAlchemyError as e:
                logger.error(f"Error while adding new line in Urls table: {e}")
                return False

            logger.info(f"compared new urls: {user_url} -> {short_url}")

            session.commit()

        return True

    async def get_user_by_short(self, short_url):
        with Session(self.engine) as session:
            req = select(Urls.user_url).where(Urls.short_url == short_url)

            try:
                user_url = session.scalars(req).one()
            except SQLAlchemyError as e:
                logger.error(
                    f"Error while getting user url by short url from Urls table: {e}"
                )
                return None

            logger.info(
                f"short url {short_url} is compare to user url {user_url}"
            )

        return user_url

    async def get_short_by_user(self, user_url):
        with Session(self.engine) as session:
            req = select(Urls.short_url).where(Urls.short_url == user_url)

            try:
                short_url = session.scalars(req).one()
            except SQLAlchemyError as e:
                logger.error(
                    f"Error while getting short url by user url from Urls table: {e}"
                )
                return None

            logger.info(
                f"user url {user_url} is compare to short url {short_url}"
            )

        return short_url
