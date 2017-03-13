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