from flask import Flask
from flask import request, jsonify, redirect
from os import environ as e
app = Flask("neko")

@app.route('/')
def redirect ():
 return redirect("https://roseloverx.me")

@app.route('/screenshot')
def ss():
 q = request.args.get("url")
 if not q:
   return jsonify({"status": 400, "error": "url parameter not provided."})
 

def ping():
 return jsonify({"status": "ok", "author": "RoseLovErX"})


app.add_url_rule("/ping", "ping", ping, methods=['GET'])

app.run(host='0.0.0.0', port=e.get("PORT"), threaded=True)
