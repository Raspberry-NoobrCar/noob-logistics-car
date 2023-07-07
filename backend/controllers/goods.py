from flask_socketio import SocketIO

def init(ws: SocketIO):

    @ws.on('message')
    def handle_message(type, data: dict):
        print(f'[{type}]received message: ' + data["data"])
