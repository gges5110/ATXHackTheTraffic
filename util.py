from __future__ import print_function
import sys

def console_print(string):
    print(string, file=sys.stderr)

def time_list():
    timeList = []
    for i in range(0, 4*24):
        if (i % 4) * 15 == 0:
            timeList.append(str(i / 4) + ":00")
        else:
            timeList.append(str(i / 4) + ":" + str((i % 4) * 15))
    return timeList

def weekday_list():
    weekdayList = []
    weekdayList.append('Monday')
    weekdayList.append('Tuesday')
    weekdayList.append('Wednesday')
    weekdayList.append('Thursday')
    weekdayList.append('Friday')
    weekdayList.append('Saturday')
    weekdayList.append('Sunday')
    return weekdayList

def FindRoadConnectToCorridor(travelsensors):
    latitude = []
    longitude = []
    readerID = []
    for sensor in travelsensors:
        latitude.append(sensor.LATITUDE)
        longitude.append(sensor.LONGITUDE)
        readerID.append(sensor.READER_ID)

    if max(latitude) - min(latitude) > max(longitude) - min(longitude):
        latitude_sort = sorted(latitude)
        direction = 'Northbound'
        readerID_sort = []
        for l in latitude_sort:
            ind = latitude.index(l)
            readerID_sort.append(readerID[ind].lower())
    elif max(latitude) - min(latitude) < max(longitude) - min(longitude):
        longitude_sort = sorted(longitude)
        direction = 'Eastbound'
        readerID_sort = []
        for l in longitude_sort:
            ind = longitude.index(l)
            readerID_sort.append(readerID[ind].lower())

    return readerID_sort, direction

def CheckConnection(data_summary,corridor_intersection_all):

    ODpair = []
    for data in data_summary:
        ODpair.append(data.Origin.lower()+data.Destination.lower())

    corridor_intersection = []
    skip = False
    for i in range(len(corridor_intersection_all)-1):
        if skip:
            if next_intersection == corridor_intersection_all[i]:
                skip = False
            else:
                continue
        x = corridor_intersection_all[i]+corridor_intersection_all[i+1]

        # Pair of intersections with data are included
        if x in ODpair and i < len(corridor_intersection_all) - 2:
            corridor_intersection.append(corridor_intersection_all[i])
        # end condition
        elif x in ODpair and i == len(corridor_intersection_all) - 2:
            corridor_intersection.append(corridor_intersection_all[i])
            corridor_intersection.append(corridor_intersection_all[i+1])
        # Search for next pair of intersections with data
        else:
            n = i
            while (n < len(corridor_intersection_all)-2 and x not in ODpair):
                n = n+1
                x = corridor_intersection_all[i]+corridor_intersection_all[n+1]

            if x in ODpair:
                corridor_intersection.append(corridor_intersection_all[i])
                next_intersection = corridor_intersection_all[n+1]
                skip = True
    return corridor_intersection

def example_function():
    return "return value"
