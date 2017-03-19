from util import console_print
from flask import Blueprint, render_template, request
from database_setup import Base, User, TravelSensor, db_session, Summary
from sqlalchemy.orm import aliased

historyStats = Blueprint('historyStats', __name__)

@historyStats.route("/historyStats", methods=['GET'])
def historyStats_function():

    # Generate display strings for frontend.
    startTimeList = []
    for i in range(0, 4*24):
        if (i % 4) * 15 == 0:
            startTimeList.append(str(i / 4) + ":00")
        else:
            startTimeList.append(str(i / 4) + ":" + str((i % 4) * 15))
    
    weekdayList = []
    weekdayList.append('Monday')
    weekdayList.append('Tuesday')
    weekdayList.append('Wednesday')
    weekdayList.append('Thursday')
    weekdayList.append('Friday')
    weekdayList.append('Saturday')
    weekdayList.append('Sunday')

    # Parse request params and set default values.
    year = request.args.get('year')
    if year is None:
        year = 2016
    else:
        year = int(year)

    weekday = request.args.get('weekday')
    if weekday is None:
        weekday = 0
    else:
        weekday = int(weekday)

    time = request.args.get('time')
    start_time = 0
    if time is None:
        time = 0
    else:
        start_time = int(time)
        time = (int(time) - 1) * 15

    # Query database for average travel time and travel sensor geographic data.
    origin = aliased(TravelSensor, name='origin')
    destination = aliased(TravelSensor, name='destination')

    result = db_session.query(Summary.Origin, Summary.Destination, Summary.Time, Summary.Weekday, Summary.Avg_Travel_Time, origin, destination).\
        join(origin, Summary.Origin == origin.READER_ID).\
        join(destination, Summary.Destination == destination.READER_ID).\
        filter(Summary.Weekday == weekday, Summary.Time == time, Summary.Year == year)

    traffic_list = result.all()
    # console_print("result count: " + str(result.count()))
    # console_print("result count: " + str(result.column_descriptions))

    return render_template("historyStats.html", traffic_list=traffic_list, startTimeList=startTimeList, start_time=start_time, weekdayList=weekdayList, weekday=weekday)
