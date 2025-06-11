import aiohttp_jinja2
import logging
from aiohttp import web

from url_shortener.utils.validator import validate_url
from url_shortener.utils.trans_url import TransUrl

tr_url = TransUrl()

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template("home.html")
async def home(request):
    if request.method == "POST":
        data = await request.post()
        user_url = data["user_url"]
        logger.info(f"user_url: {user_url}")

        is_cor_url = await validate_url(user_url)
        if not is_cor_url:
            return {"bad_url": True}

        new_url = await tr_url.get_short_url()
        return {"new_url": new_url}

    return {}


@aiohttp_jinja2.template("urls.html")
async def urls(request):
    url = request.match_info.get("url", "bad_url")
    logger.info(f"url: {url}")

    # достаем из базы соотв url
    redirect_url = "https://docs.aiohttp.org/en/stable/web_quickstart.html"

    if redirect_url is None:
        redirect_url = "http//:localhost:8080/"

    raise web.HTTPFound(redirect_url)
