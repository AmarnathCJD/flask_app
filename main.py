from flask import Flask
from flask import request, jsonify
app = Flask("neko")

def ping():
 return jsonify({"status": "ok", "author": "RoseLovErX"})

@app.add_url_rule("/ping", "ping", ping, methods=['GET'])
