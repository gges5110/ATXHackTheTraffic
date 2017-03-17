from flask import Blueprint, render_template
from CorridorTravelTime import corridor_traveltime

heatmap = Blueprint('heatmap', __name__)

@heatmap.route("/heatmap", methods=['GET'])
def heatmap_function():
    startTimeList = []
    for i in range(0, 4*24):
        if (i % 4) * 15 == 0:
            startTimeList.append(str(i / 4) + ":00")
        else:
            startTimeList.append(str(i / 4) + ":" + str((i % 4) * 15))

    Corridor_name = 'lamar'
    year_selected = 2016
    weekday_selected = 0 # Monday is 0
    [Normalized_traveltime, Average_traveltime, Direction, Corridor_intersection] = corridor_traveltime(Corridor_name, year_selected, weekday_selected)
    datamatrix=[]
    for i in range(0, len(startTimeList)-1):
        for j in range(0,len(Corridor_intersection[0])-2):
            if Normalized_traveltime[0][j][i] <= 0.000000001:
                Normalized_traveltime[0][j][i] = 0
            datamatrix.append(tuple([i,j,Normalized_traveltime[0][j][i]]))
    return render_template("heatmap.html", startTimeList=startTimeList, traveltime_N=Normalized_traveltime , traveltime_bar=Average_traveltime, Direction=Direction, Corridor_intersection=Corridor_intersection, result=datamatrix)
