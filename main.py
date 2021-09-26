from os import environ as e
from os import remove
from time import sleep

from flask import Flask, jsonify, request
from flask.helpers import send_file
from selenium import webdriver

from utils import google_search, imdb_search

app = Flask("neko")
app.config["JSON_SORT_KEYS"] = False

api_key_demo = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"


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

app.run(host="0.0.0.0", port=e.get("PORT"), threaded=True)

import contextlib

from lona import LonaApp, LonaView
from lona.html import H1, HTML, Button, NumberInput, Span

app2 = LonaApp("lona")


@app.route("/")
class CounterView(LonaView):
    def handle_request(self, request):
        counter = Span("0")
        number_input = NumberInput(value=10, _style={"width": "3em"})
        html = HTML(
            H1("Counter: ", counter),
            number_input,
            Button("Set", _id="set"),
            Button("Decrease", _id="decrease", _style={"margin-left": "1em"}),
            Button("Increase", _id="increase"),
        )

        while True:
            self.show(html)

            input_event = self.await_click()
            if input_event.node_has_id("increase"):
                counter.set_text(
                    int(counter.get_text()) + 1,
                )
            elif input_event.node_has_id("decrease"):
                counter.set_text(
                    int(counter.get_text()) - 1,
                )
            elif input_event.node_has_id("set"):
                with contextlib.suppress(TypeError):
                    counter.set_text(int(number_input.value))


app2.run(port=e.get("PORT"), host="0.0.0.0")
# later
# will fix lona addon
