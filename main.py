from flask import Flask
from flask import request, jsonify
import os
print(os.environ.get("PORT"))
app = Flask("neko")

def ping():
 return jsonify({"status": "ok", "author": "RoseLovErX"})

app.add_url_rule("/ping", "ping", ping, methods=['GET'])

app.debug = True
app.run(port=$PORT)
