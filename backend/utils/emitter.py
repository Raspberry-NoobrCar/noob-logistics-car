from flask_socketio import SocketIO

class Emitter:
    def __init__(self, ws: SocketIO):
        self.ws = ws

    def loadGood(self, good):
        self.ws.emit("loadGood", good)

    def unLoadGood(self, good):
        self.ws.emit("unloadGood", good)

    def setPath(self, path):
        self.ws.emit("setPath", path)

    def handleError(self, error):
        self.ws.emit('handleError',error)

    def handleMove(self, data: dict):
        self.ws.emit("handleMove", data)

    def setBarrier(self, xy: dict):
        self.ws.emit("setBarrier", xy)

    def setTrafficSign(self, data: dict):
        self.ws.emit("setTrafficSign", data)