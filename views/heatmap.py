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
    # Normalized_traveltime: contains Z-score of traveltime (drawing color base on this.) N[0]: N or E N[1]: S bound
    # Average_traveltime: contains raw traveltime (drawing color base on this.) N[0]: N or E N[1]: S bound
    # Direction: D[0]: "Northbound" or "Eastbound"
    # Corridor_intersection: C[0] = ['lamar&1','lamar&2',...,'lamar&last']
    datamatrix=[]
    datamatrix_second=[]
    for i in range(0, len(startTimeList)-1):
        for j in range(0,len(Corridor_intersection[0])-2):
            if Normalized_traveltime[0][j][i] <= 0.000000001:
                Normalized_traveltime[0][j][i] = 0
            datamatrix.append(tuple([i,j,Normalized_traveltime[0][j][i]]))
        for j in range(0,len(Corridor_intersection[1])-2):
            if Normalized_traveltime[1][j][i] <= 0.000000001:
                Normalized_traveltime[1][j][i] = 0
            datamatrix_second.append(tuple([i,j,Normalized_traveltime[1][j][i]]))
    return render_template("heatmap.html", startTimeList=startTimeList, traveltime_N=Normalized_traveltime , traveltime_bar=Average_traveltime, Direction=Direction, Corridor_intersection=Corridor_intersection, result=datamatrix, result2=datamatrix_second)
