import aiohttp_jinja2
import logging
from aiohttp import web

from url_shortener.utils.validator import validate_url
from url_shortener.utils.trans_url import TransUrl
from url_shortener.db.urls_repo import UrlsRepo
from url_shortener.db.conn_to_db import init_db

urls_repo = UrlsRepo(init_db())

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
            return {
                "flashed_message": "Введен не корректный url",
                "message_status": "alert-danger",
            }

        new_url = await tr_url.get_short_url()

        is_good = await urls_repo.compare_urls(user_url, new_url)
        if not is_good:
            return {
                "flashed_message": "Не удалось создать новый url",
                "message_status": "alert-danger",
            }

        return {
            "flashed_message": "Короткий url успешно создан",
            "message_status": "alert-success",
            "new_url": new_url,
        }

    return {}


@aiohttp_jinja2.template("urls.html")
async def urls(request):
    short_url = "http://localhost:8080/urls/" + request.match_info.get(
        "url", "bad_url"
    )

    user_url = await urls_repo.get_user_by_short(short_url)

    if user_url is None:
        user_url = "http://localhost:8080/bad_url"

    raise web.HTTPFound(user_url)


@aiohttp_jinja2.template("bad_url.html")
async def bad_url(request):
    return {}
