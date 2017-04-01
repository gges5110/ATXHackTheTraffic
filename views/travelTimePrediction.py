from util import time_list, weekday_list
from flask import Blueprint, render_template, request
from database_setup import Base, TravelSensor, Summary
from database_init import db_session
from route import time_prediction

travelTimePrediction = Blueprint('travelTimePrediction', __name__)

@travelTimePrediction.route("/travelTimePrediction", methods=['GET', 'POST'])
def travelTimePrediction_function():
    travelSensors = db_session.query(TravelSensor).all()
    startTimeList = time_list()
    weekdayList = weekday_list()
    time_pre = None
    origin = 'congress_oltorf'
    destination = 'congress_11th'
    start_time = 37
    weekday = 0

    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        start_time = int(request.form['start_time'])
        weekday = int(request.form['weekday'])
        minutes = (start_time - 1) * 15
        time_pre = time_prediction.findRoute(origin, destination, minutes, weekday)
        if time_pre['time'] != -1:
            time_pre['time'] = round(time_pre['time']/60, 2)

    return render_template("travelTimePrediction.html", travelSensors=travelSensors, time_pre=time_pre, startTimeList=startTimeList, weekdayList=weekdayList, weekday=weekday, origin = origin, destination = destination, start_time = start_time)
