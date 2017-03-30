from flask import Blueprint, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, TravelSensor, Summary
from database_init import db_session
import util

index = Blueprint('index', __name__)

@index.route("/", methods=['GET'])
def index_function():
    user = db_session.query(User).first()
    travelSensors = db_session.query(TravelSensor).all()
    return_from_util = util.example_function()
    print travelSensors[0].READER_ID
    summary = db_session.query(Summary).filter(Summary.Origin == "51st_manor").all()
    print summary[0].Time
    return render_template("index.html", user=user, msg=None)
