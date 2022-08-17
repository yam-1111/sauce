
from flask import Flask, render_template
from os import system
from threading import Thread
from settings.server_config import launcher

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.get("/")
def index():
    return render_template("index.html")

def start():
    app.run(host="0.0.0.0", port=8080)

def standalone_player():
      system('cd router && java -jar Lavalink.jar')

def keep_run(standalone=False):
    t1 = Thread(target=start)
    t2 = Thread(target=standalone_player)
    if standalone is True:
        t2.start()
    t1.start()