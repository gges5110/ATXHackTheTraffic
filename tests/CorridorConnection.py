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
        readerID_sort = []
        for l in latitude_sort:
            ind = latitude.index(l)
            readerID_sort.append(readerID[ind].lower())
    elif max(latitude) - min(latitude) < max(longitude) - min(longitude):
        longitude_sort = sorted(longitude)
        readerID_sort = []
        for l in longitude_sort:
            ind = longitude.index(l)
            readerID_sort.append(readerID[ind].lower())

    return readerID_sort

def CheckConnection(data_summary,corridor_intersection_all):

    ODpair = []
    for data in data_summary:
        ODpair.append(data.Origin.lower()+data.Destination.lower())

    corridor_intersection = []
    for i in range(len(corridor_intersection_all)-1):
        x = corridor_intersection_all[i]+corridor_intersection_all[i+1]
        print(x)
        # Pair of intersections with data are included
        if x in ODpair and i < len(corridor_intersection_all) - 1:
            corridor_intersection.append(corridor_intersection_all[i])
        # end condition
        elif x in ODpair and i == len(corridor_intersection_all) - 1:
            corridor_intersection.append(corridor_intersection_all[i])
            corridor_intersection.append(corridor_intersection_all[i+1])
        # Search for next pair of intersections with data
        else:
            n = i
            while (n < len(corridor_intersection_all)-2 and x not in ODpair):
                n = n+1
                x = corridor_intersection_all[i]+corridor_intersection_all[n+1]

            if x in ODpair and n < len(corridor_intersection_all)-1:
                corridor_intersection.append(corridor_intersection_all[i])

    return corridor_intersection

    return