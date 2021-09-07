from flask import Flask
from flask import request, jsonify
from os import environ as e
app = Flask("neko")

def ping():
 return jsonify({"status": "ok", "author": "RoseLovErX"})

app.add_url_rule("/ping", "ping", ping, methods=['GET'])

app.run(host='0.0.0.0', port=e.get("PORT"), threaded=True)
