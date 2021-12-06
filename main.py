from os import environ as e

from flask import Flask, jsonify, request
from telethon import TelegramClient

app = Flask("neko")
app.config["JSON_SORT_KEYS"] = False

api_key = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"
bot = TelegramClient(
    "api_bot",
    4529547,
    "55bc2f0ca39d588ce5471e52acbf5a69",
)
bot.start(bot_token="2119405816:AAGu8VU68vVHqbWsc0VsHSXWzgcbZwxyClk")

"""
@app.route("/screenshot")
def ss():
    q = request.args.get("url")
    timeout = request.args.get("timeout", 0)
    if not timeout.isnumeric():
        timeout = 0
    else:
        timeout = int(timeout)
    if not q:
        return jsonify({"status": 400, "error": "url parameter not provided."})
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.get(q)
        driver.set_window_size(1280, 720)
        if timeout:
            sleep(timeout)
        img = driver.get_screenshot_as_png()
        driver.close()
    except Exception as e:
        e = str(e).replace("\n", "")
        return jsonify({"status": 401, "error": e})
    with open("image.png", "wb") as file:
        file.write(img)
    return send_file("image.png", mimetype="image/png")
    remove("image.png")


@app.route("/imdb")
def imdb_search():
    q = request.args.get("title")
    if not q:
        return jsonify({"status": 400, "error": "query parameter not provided."})
    result = imdb_search(q)
    return jsonify({"status": "ok", "result": result})


@app.route("/google")
def google_search_query():
    query = request.args.get("query")
    limit = request.args.get("limit", "5")
    if not limit.isdigit():
        return jsonify({"status": 400, "error": "limit is not a valid integer."})
    if not query:
        return jsonify({"status": 400, "error": "query parameter not provided."})
    results = google_search(query, int(limit))
    return jsonify({"status": "ok", "results": results})


def ping():
    return jsonify({"status": "ok", "author": "RoseLovErX"})


app.add_url_rule("/ping", "ping", ping, methods=["GET"])
"""


@app.route("/username")
async def resolve_username():
    q = request.args.get("u")
    if not q:
        return jsonify({"status": 401, "error": "username is empty"})
    try:
        u = await bot.get_entity(q)
        await bot.send_message("RoseLoverX", "test1")
        print(u.first_name)
        return jsonify({"status": 200, "entity": str(u.first_name)})
    except Exception as a:
        return jsonify({"status": 403, "error": str(a)})


app.run(host="0.0.0.0", port=e.get("PORT"), threaded=True)
bot.run_until_disconnected()
