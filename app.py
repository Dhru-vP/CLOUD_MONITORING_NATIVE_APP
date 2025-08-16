import psutil
from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def get_metrics():
    while True:
        cpu_metric = psutil.cpu_percent()
        mem_metric = psutil.virtual_memory().percent
        message = "High CPU or Memory Detected, scale up!!!" if cpu_metric > 80 or mem_metric > 80 else None

        socketio.emit("update_metrics", {"cpu_metric": cpu_metric, "mem_metric": mem_metric, "message": message})
        time.sleep(0.5) 

@app.route("/")
def index():
    """Render the index page."""
    return render_template("index.html", cpu_metric=0, mem_metric=0, message=None)

@socketio.on("connect")
def handle_connect():
    """Start background thread when a client connects."""
    socketio.start_background_task(get_metrics)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
