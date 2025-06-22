import aiohttp_jinja2
import logging
from aiohttp import web

from url_shortener.utils.validator import validate_url

logger = logging.getLogger(__name__)


class Views:
    def __init__(self, urls_repo=None, tr_url=None):
        self.urls_repo = urls_repo
        self.tr_url = tr_url

    @aiohttp_jinja2.template("home.html")
    async def home(self, request):
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

            short_url = await self.urls_repo.get_short_by_user(user_url)
            if short_url is not None:
                return {
                    "flashed_message": "Короткий url успешно создан",
                    "message_status": "alert-success",
                    "new_url": short_url,
                }

            new_url = await self.tr_url.get_short_url()

            is_good = await self.urls_repo.compare_urls(user_url, new_url)
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

    async def urls(self, request):
        short_url = "http://localhost:8080/urls/" + request.match_info.get(
            "url", "bad_url"
        )

        user_url = await self.urls_repo.get_user_by_short(short_url)

        if user_url is None:
            user_url = "http://localhost:8080/bad_url"

        raise web.HTTPFound(user_url)

    @aiohttp_jinja2.template("error_page.html")
    async def bad_url(self, request):
        return {
            "image": "https://i.pinimg.com/736x/6d/a8/e6/6da8e6d1456bfb1345cfaedf4690448e.jpg",
            "h1": "Похоже этот url не привязан к другому сайту",
            "lead": "Вы можете сократить нужный вам url на главной странице",
        }
