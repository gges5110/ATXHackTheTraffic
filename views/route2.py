from flask import Blueprint

route2 = Blueprint('route2', __name__)

@route2.route("/route2")
def route2_function():
    return "route2!"
