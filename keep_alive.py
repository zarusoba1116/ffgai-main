import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run(port):
    app.run(host="0.0.0.0", port=port)

def keep_alive(port=8080):
    t = Thread(target=run, args=(port,))
    t.start()