from flask import Blueprint, render_template
from database_setup import Base, User, TravelSensor, db_session, Summary

historyStats = Blueprint('historyStats', __name__)

@historyStats.route("/historyStats", methods=['GET'])
def historyStats_function():    
    return render_template("historyStats.html")
