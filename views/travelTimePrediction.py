from util import time_list
from flask import Blueprint, render_template, request
from database_setup import Base, TravelSensor, Summary
from database_init import db_session
from route import time_prediction

travelTimePrediction = Blueprint('travelTimePrediction', __name__)

@travelTimePrediction.route("/travelTimePrediction", methods=['GET', 'POST'])
def travelTimePrediction_function():
    travelSensors = db_session.query(TravelSensor).all()
    startTimeList = time_list()

    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        start_time = int(request.form['start_time'])
        minutes = (start_time - 1) * 15
        time_pre = time_prediction.findRoute(origin, destination, minutes, 0)
        return render_template("travelTimePrediction.html", travelSensors=travelSensors, time_pre=time_pre, startTimeList=startTimeList, origin = origin, destination = destination, start_time = start_time)
        # return render_template("travelTimePrediction.html", travelSensors=travelSensors, startTimeList=startTimeList, origin = origin, destination = destination, start_time = start_time)
    else:
        return render_template("travelTimePrediction.html", travelSensors=travelSensors, time_pre=None, startTimeList=startTimeList)
