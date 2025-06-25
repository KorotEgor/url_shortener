import aiohttp_jinja2
from aiohttp import web
import logging

logger = logging.getLogger(__name__)


async def handle_404(request):
    return aiohttp_jinja2.render_template(
        "error_page.html",
        request,
        {
            "image": "https://mem-tube.ru/web/loads/image/vy-kto-takie.jpg",
            "h1": "Ошибочка 404",
            "lead": "Тут ничего нет. Возвращайся на главную",
        },
        status=404,
    )


async def handle_500(request):
    return aiohttp_jinja2.render_template(
        "error_page.html",
        request,
        {
            "image": "https://pressa.tv/uploads/posts/2019-08/1567112675_pressa_tv_prikolnye_foto_28.jpg",
            "h1": "Ошибочка 500",
            "lead": "Я где-то накосячил, ноя уже решаю эту проблему",
        },
        status=500,
    )


def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except Exception:
            request.protocol.logger.exception("Error handling request")
            return await handle_500(request)

    return error_middleware


def setup_error_middleware(app):
    error_middleware = create_error_middleware(
        {
            404: handle_404,
            500: handle_500,
        }
    )
    app.middlewares.append(error_middleware)
