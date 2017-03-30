from flask import Blueprint, render_template
from database_setup import User, TravelSensor, Summary
from database_init import db_session

index = Blueprint('index', __name__)

@index.route("/", methods=['GET'])
def index_function():
    user = db_session.query(User).first()
    travelSensors = db_session.query(TravelSensor).all()
    print travelSensors[0].READER_ID
    summary = db_session.query(Summary).filter(Summary.Origin == "51st_manor").all()
    print summary[0].Time
    return render_template("index.html", user=user, msg=None)
