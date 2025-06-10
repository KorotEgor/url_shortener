import aiohttp_jinja2
import logging

from url_shortener.validator import validate_url

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template("home.html")
async def home(request):
    if request.method == "POST":
        data = await request.post()
        user_url = data["user_url"]

        is_cor_url = await validate_url(user_url)
        if not is_cor_url:
            return {"bad_url": True}

        logger.info(f"user_url: {user_url}")
        return {"new_url": "http//:localhost:8080/urls/"}

    return {}
