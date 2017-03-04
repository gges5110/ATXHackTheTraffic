from flask import Blueprint, render_template

travelTimePrediction = Blueprint('travelTimePrediction', __name__)

@travelTimePrediction.route("/travelTimePrediction", methods=['GET'])
def travelTimePrediction_function():
    return render_template("travelTimePrediction.html")
