import asyncio
import os

from aiohttp import web
from google_translate_py import AsyncTranslator
from telethon import TelegramClient, types

from home import HOME
from utils import google_search, imdb_search

routes = web.RouteTableDef()

api_key_demo = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"

bot = TelegramClient(
    "api_bot",
    os.getenv("APP_ID"),
    os.getenv("API_HASH"),
)
bot.start(bot_token=os.getenv("TOKEN"))


@routes.get("/")
async def base(r):
    return web.Response(text=HOME, content_type="text/html")


"""
    a = time.time()
    return web.json_response(
        {"status": 200, "ping": str(time.time() - a)[:3] + " ms"},
        content_type="application/json",
        status=200,
    )
"""

@routes.get("/go")
async def go_ev(r):
    try:
        code = r.rel_url.query["code"]
    except KeyError:
        return web.json_response(
        {"error": "'code' param is empty"}, content_type="application/json", status=403
    )
    eval = go_eval(code)
    return web.json_response(
        eval, content_type="application/json", status=200
    )

@routes.get("/username")
async def uu(r):
    await r.post()
    try:
        u = await bot.get_entity(r.rel_url.query["username"])
        if isinstance(u, types.User):
            dc_id = u.photo.dc_id if u.photo else None
            return_data = {
                "id": u.id,
                "deleted": u.deleted,
                "first_name": u.first_name or "",
                "last_name": u.last_name or "",
                "username": u.username or "",
                "phone": u.phone,
                "dc_id": dc_id,
                "lang_code": u.lang_code,
                "type": "user",
            }
        elif isinstance(u, types.Channel):
            dc_id = u.photo.dc_id if u.photo else None
            return_data = {
                "id": -100 + u.id,
                "title": u.title,
                "dc_id": dc_id,
                "megagroup": u.megagroup,
                "username": u.username or "",
                "gigagroup": u.gigagroup,
                "has_link": u.has_link,
                "type": "channel",
            }
        status = 200
    except Exception as f:
        status = 503
        return_data = {"error": str(f)}
    return web.json_response(
        return_data, content_type="application/json", status=status
    )


@routes.get("/imdb")
async def IMDb(r):
    q = r.rel_url.query["q"]
    mov = imdb_search(q)
    return web.json_response(mov, content_type="application/json", status=200)


@routes.get("/translate")
async def google_trans(r):
    q, lang = r.rel_url.query["text"], r.rel_url.query["lang"]
    tr = await AsyncTranslator().translate("Hello World!!", "", lang)
    return web.json_response({"text": tr}, content_type="application/json", status=200)


@routes.get("/google")
async def gg_search(r):
    q = r.rel_url.query["query"]
    results = google_search(q)
    return web.json_response(
        {"results": results}, content_type="application/json", status=200
    )


async def start_server():
    port = int(os.environ.get("PORT"))
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()


# Server Startup
asyncio.get_event_loop().run_until_complete(start_server())
print("Web Server Started.")
bot.run_until_disconnected()
