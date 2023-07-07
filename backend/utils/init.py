from flask_socketio import SocketIO
import threading
from run import run

from .emitter import Emitter

def init(ws: SocketIO):
    emitter = Emitter(ws)
    
    # pass emitter to car-runner class

    # run car
    thread = threading.Thread(target=run, args=(emitter, ))
    thread.start()
