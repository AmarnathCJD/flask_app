from os import environ as e
import base64
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
        driver.get(q)
        img = driver.get_screenshot_as_png()
        message = "success"
    except Exception as e:
        return jsonify({"status": 401, "error": str(e)})
    img_base = str(base64.urlsafe_b64encode(img), "utf-8")
    return jsonify({"status": "ok", "message": message, "image": img})


def ping():
    return jsonify({"status": "ok", "author": "RoseLovErX"})


app.add_url_rule("/ping", "ping", ping, methods=["GET"])

app.run(host="0.0.0.0", port=e.get("PORT"), threaded=True)
