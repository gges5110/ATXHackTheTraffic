from flask import Blueprint, render_template
from database_setup import Base, User, TravelSensor, db_session, Summary

travelTimePrediction = Blueprint('travelTimePrediction', __name__)

@travelTimePrediction.route("/travelTimePrediction", methods=['GET', 'POST'])
def travelTimePrediction_function():
    travelSensors = db_session.query(TravelSensor).all()
    return render_template("travelTimePrediction.html", travelSensors=travelSensors)
