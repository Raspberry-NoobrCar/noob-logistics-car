from flask import Flask, current_app
import time

def longTask(app):
    while(True):
        ws = app.config["ws"]
        time.sleep(2)
        ws.emit("forward", "outside")
        # NOTE call car init func, emit app context