from flask import Blueprint, current_app

mapController = Blueprint('map', __name__)

@mapController.route('/api/map', methods=["GET"])
def getMap():
    current_app.config["ws"].emit("forward", "data")
    return {
        "code": 200,
        "msg": "ok",
        "data": "map"
    }
