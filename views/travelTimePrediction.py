from flask import Blueprint, render_template, request
from database_setup import Base, User, TravelSensor, db_session, Summary
# from route import time_prediction

travelTimePrediction = Blueprint('travelTimePrediction', __name__)

@travelTimePrediction.route("/travelTimePrediction", methods=['GET', 'POST'])
def travelTimePrediction_function():

    travelSensors = db_session.query(TravelSensor).all()

    if request.method == 'POST':
        time_pre = {
        'route': [u'5th_trinity', u'7th_chicon', u'7th_plesant_valley', u'7th_springdale', u'7th_shady'],
        'coord': [(30.2661324, -97.7396774), (30.2625771, -97.7221146), (30.2601261, -97.7094955), (30.2560368, -97.7016754), (30.2533531, -97.6975708)],
        'time': 466        
        }
        # origin = request.form['origin']
        # destination = request.form['destination']
        # time_pre = time_prediction.findRoute(origin, destination, 0, 0)
        return render_template("travelTimePrediction.html", travelSensors=travelSensors, time_pre=time_pre)
    else:
        return render_template("travelTimePrediction.html", travelSensors=travelSensors, time_pre=None)
