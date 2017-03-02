from flask import Blueprint, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, TravelSensor
import util

engine = create_engine('sqlite:///database1.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

route1 = Blueprint('route1', __name__)

@route1.route("/route1", methods=['GET'])
def route1_function():
    user = session.query(User).first()
    travelSensors = session.query(TravelSensor).all()
    return_from_util = util.example_function()
    print travelSensors[0].READER_ID
    return render_template("route1.html", user=user, travelSensors=travelSensors)
