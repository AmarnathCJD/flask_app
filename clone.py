import logging

from telethon import TelegramClient

API_KEY = 6
API_HASH = ""

TOKENS = []

main_bot = TelegramClient("main", API_KEY, API_HASH).start(
    bot_token=getenv("BOT_TOKEN")
)

count = 0


async def getme(client):
    BOTS[client] = await client.get_me()


BOTS = {}


def get_name(b):
    try:
        return BOTS[b].first_name
    except:
        return "Error"


cmnds = {"^/start": _start}

for tok in TOKENS:
    b = TelegramClient(str(count), API_KEY, API_HASH)
    b.start(bot_token=tok)
    count += 1
    b.run_until_complete(getme(client))
    print("Started " + BOTS[b].first_name)


def cmd(**args):
    def decorator(func):
        async def wrapper(ev):
            try:
                await func(ev)
            except Exception as exception:
                logging.info(exception)

        for a, b in BOTS:
            a.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


async def add_new_instance(tok):
    b = TelegramClient(str(count), API_KEY, API_HASH)
    b.start(bot_token=tok)
    b.run_until_complete(getme(client))
    print("Started " + BOTS[b].first_name)
    for x, y in cmnds:

        async def wrapper(ev):
            try:
                await y(ev)
            except Exception as exception:
                logging.info(exception)

        b.add_event_handler(wrapper, events.NewMessage(pattern=x))


@cmd(pattern="^/tok ?(.*)")
async def add_tok(e):
    if len(e.text.split(" ") > 1):
        if not ":" in e.text.split(" ", maxsplit=2)[1]:
            return await e.reply("Eeee erong format.")
    else:
        return await e.reply("No token found.")
    await add_new_instance(e.text.split(" ", maxsplit=1)[1])


@cmd(pattern="^/start")
async def _start(e):
    await e.reply("Test clone bot named as {}".format(get_name(e.client)))


main_bot.run_until_disconnected()
