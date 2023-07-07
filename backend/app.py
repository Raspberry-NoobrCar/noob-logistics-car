from utils.init import init
from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from controllers.map import mapController
from controllers.hello import helloController
import controllers.goods as goodsController

def createApp():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'secret'

    app.register_blueprint(mapController)
    app.register_blueprint(helloController)

    socketio = SocketIO(app, cors_allowed_origins="*")
    app.config["ws"] = socketio

    goodsController.init(socketio)

    ws: SocketIO = app.config["ws"]
    init(ws)

    return app
