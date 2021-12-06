import asyncio
import os

from aiohttp import web
from telethon import TelegramClient, types

routes = web.RouteTableDef()

api_key = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"
bot = TelegramClient(
    "api_bot",
    4529547,
    "55bc2f0ca39d588ce5471e52acbf5a69",
)
bot.start(bot_token="2119405816:AAGu8VU68vVHqbWsc0VsHSXWzgcbZwxyClk")
bot.start()


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
                "first_name": u.first_name,
                "last_name": u.last_name,
                "username": u.username,
                "phone": u.phone,
                "dc_id": dc_id,
                "lang_code": u.lang_code,
                "type": "user",
            }
            status = 200
    except Exception as f:
        print(f)
    return web.json_response(return_data, content_type="application/json", status=status)


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
