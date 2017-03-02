from flask import Blueprint

route3 = Blueprint('route3', __name__)

@route3.route("/route3", methods=['GET'])
def route3_function():
    return "route3!"
