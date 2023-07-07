from flask import Blueprint, current_app

helloController = Blueprint("hello", __name__)

@helloController.route("/hello", methods=["GET"])
def handleHello():
    return {
        "msg": "hello"
    }