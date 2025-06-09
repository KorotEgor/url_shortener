import aiohttp_jinja2


@aiohttp_jinja2.template("home.html")
async def home(request):
    return {}
