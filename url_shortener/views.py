import aiohttp_jinja2
import logging
from aiohttp import web

from url_shortener.utils.validator import validate_url
from url_shortener.utils.trans_url import TransUrl
from url_shortener.db.conn_to_db import get_db

urls_repo = get_db()

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

        short_url = await urls_repo.get_short_by_user(user_url)
        if short_url is not None:
            return {
                "flashed_message": "Короткий url успешно создан",
                "message_status": "alert-success",
                "new_url": short_url,
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


@aiohttp_jinja2.template("error_page.html")
async def bad_url(request):
    return {
        "image": "https://i.pinimg.com/736x/6d/a8/e6/6da8e6d1456bfb1345cfaedf4690448e.jpg",
        "h1": "Похоже этот url не привязан к другому сайту",
        "lead": "Вы можете сократить нужный вам url на главной странице",
    }
