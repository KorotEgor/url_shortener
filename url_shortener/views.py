import aiohttp_jinja2
import logging

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template("home.html")
async def home_get(request):
    return {}


@aiohttp_jinja2.template("home.html")
async def home_post(request):
    data = await request.post()
    user_url = data["user_url"]
    logger.info(f"user_url: {user_url}")
    return {"new_url": "http//:localhost:8080/urls/"}
