from flask import Blueprint, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, TravelSensor, db_session
import util

index = Blueprint('index', __name__)

@index.route("/", methods=['GET'])
def index_function():
    user = db_session.query(User).first()
    travelSensors = db_session.query(TravelSensor).all()
    return_from_util = util.example_function()
    print travelSensors[0].READER_ID
    return render_template("index.html", user=user, msg=None)
