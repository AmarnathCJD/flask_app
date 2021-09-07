from os import environ as e

from flask import Flask, jsonify, redirect, request
from selenium import webdriver

app = Flask("neko")

api = "e860abbe-0fe5-11ec-bb0a-36f5724811b8"


@app.route("/")
def redirect():
    return redirect("https://roseloverx.me")


@app.route("/screenshot")
def ss():
    q = request.args.get("url")
    if not q:
        return jsonify({"status": 400, "error": "url parameter not provided."})
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        pq = "sucess"
    except Exception as e:
        pq = e
    return jsonify({"status": "ok", "test": pq})


def ping():
    return jsonify({"status": "ok", "author": "RoseLovErX"})


app.add_url_rule("/ping", "ping", ping, methods=["GET"])

app.run(host="0.0.0.0", port=e.get("PORT"), threaded=True)
