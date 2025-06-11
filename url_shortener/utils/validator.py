import logging
from pydantic import BaseModel, HttpUrl, ValidationError

logger = logging.getLogger(__name__)


class MyModel(BaseModel):
    url: HttpUrl


async def validate_url(url):
    try:
        HttpUrl(url)
    except ValidationError as e:
        logger.info(f"Неверный URL ({url}): {e}")
        return False
    return True
