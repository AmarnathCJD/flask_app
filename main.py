from os import environ as e
from os import remove
from time import sleep

from flask import Flask, jsonify, redirect, request
from flask.helpers import send_file
from selenium import webdriver

from utils import imdb

app = Flask("neko")

api = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"


@app.route("/")
def redirect():
    return redirect("https://roseloverx.me")


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
    result = imdb(q)
    return jsonify({"status": "ok", "result": result})


@app.route("/google")
def google_search():
    query = request.args.get("query")
    if not query:
        return jsonify({"status": 400, "error": "query parameter not provided."})
    return jsonify({"status": "ok", "message": "soon"})


def ping():
    return jsonify({"status": "ok", "author": "RoseLovErX"})


app.add_url_rule("/ping", "ping", ping, methods=["GET"])

app.run(host="0.0.0.0", port=e.get("PORT"), threaded=True)
