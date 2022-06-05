import asyncio
import os

os.system("pip3 install youtube-search-python")

from aiohttp import web
from google_translate_py import AsyncTranslator
from requests import get
from telethon import TelegramClient, types

from utils import go_eval, google_search, imdb_search, paste, sed, yt_search

routes = web.RouteTableDef()

# bot = TelegramClient(
    "null",
    os.getenv("APP_ID"),
    os.getenv("API_HASH"),
)
# api = TelegramClient(
    "api",
    os.getenv("APP_ID"),
    os.getenv("API_HASH"),
)
# bot.start(bot_token=os.getenv("TOKEN"))
# api.start(bot_token=os.getenv("BOT_TOKEN"))


@routes.get("/")
async def base_page(r):
    return web.json_response(
            {"message": "'welcome to roseAPI'"},
            content_type="application/json",
            status=200,
        )

@routes.get("/go")
async def go_ev(r):
    try:
        code = r.rel_url.query["code"]
    except KeyError:
        return web.json_response(
            {"error": "'code' param is empty"},
            content_type="application/json",
            status=403,
        )
    eval = go_eval(code)
    return web.json_response(eval, content_type="application/json", status=200)


@routes.get("/username")
async def uu(r):
    await r.post()
    try:
        u = await api.get_entity(r.rel_url.query["username"])
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


@routes.get("/paste")
async def paste_nekobin(r):
    data = r.rel_url.query
    try:
        text = data["text"]
    except KeyError:
        return web.json_response(
            {"error": "no text param given"},
            content_type="application/json",
            status=401,
        )
    p = paste(text)
    return web.json_response(p, content_type="application/json", status=200)


cm = ""


@routes.post("/git")
async def git_webhook(r):
    global cm
    cm = await r.json()
    try:
        s = cm.get("data").get("status")
        if s == "failed":
            d = cm.get("data").get("output_stream_url")
            with get(d) as r:
                data = r.text.split("#")[1]
                await bot.send_message(
                    "roseloverx_support",
                    "<b><u>Heroku Build Failed</u></b>, \n<b>LOGS:</b> \n" + str(data),
                    parse_mode="html",
                )
    except BaseException as a:
        print(a)
    return web.json_response(
        {"success": True}, content_type="application/json", status=200
    )


@routes.get("/webhook")
async def c(r):
    return web.Response(text=str(cm))


@routes.get("/sed")
async def sed_py_(r):
    d = r.rel_url.query["text"]
    ed = r.rel_url.query["sed"]
    if not d:
        return web.json_response(
            {"err": "error"}, content_type="application/json", status=200
        )
    sad = sed(d, ed)
    return web.json_response(sad, content_type="application/json", status=200)


@routes.get("/youtube")
async def yt_s(r):
    try:
        q = r.rel_url.query["q"]
    except KeyError:
        return web.json_response({"error": "q param not found"}, status=501)
    search = yt_search(q, 10)
    return web.json_response(search, status=200)


async def start_server():
    port = 5400
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()


# Server Startup
asyncio.get_event_loop().run_until_complete(start_server())
print("Web Server Started.")
bot.run_until_disconnected()
