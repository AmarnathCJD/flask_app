from aiohttp import web
from telethon import TelegramClient

routes = web.RouteTableDef()

api_key = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"
bot = TelegramClient(
    "api_bot",
    4529547,
    "55bc2f0ca39d588ce5471e52acbf5a69",
)
bot.start(bot_token="2119405816:AAGu8VU68vVHqbWsc0VsHSXWzgcbZwxyClk")
bot.start()


@routes.get("/")
async def uu(r):
    return web.Response(text=str(bot.get_me()))
