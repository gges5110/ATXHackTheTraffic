from context import TravelSensor, Summary, init_db
db_session = init_db()
# Database model definition in database_setup.py


# Test for TravelSensor data model
travelSensorsCount = db_session.query(TravelSensor).count()
print "Travel Sensor Entry Count:", travelSensorsCount

travelSensors_test1 = db_session.query(TravelSensor).all()
for sensor in travelSensors_test1:
    print sensor.READER_ID, sensor.LATITUDE, sensor.LONGITUDE

# primary_st = "WILLIAM CANNON DR"
# print ""
# print "Travel Sensor with PRIMARY_ST =", primary_st
# travelSensors_test2 = db_session.query(TravelSensor).filter_by(PRIMARY_ST=primary_st).all()
# # If you use .all(), you will get a list of TravelSensor objects.
# for sensor in travelSensors_test2:
#     print sensor.READER_ID, sensor.LATITUDE, sensor.LONGITUDE

lat = 30.3
print ""
print "Fetch the first sensor with latitude greater than", lat
travelSensors_test3 = db_session.query(TravelSensor).filter(TravelSensor.LATITUDE > lat).first()
# Notice that if you use .first(), it will be an object and not a list.
if travelSensors_test3 is not None:
    print travelSensors_test3.READER_ID, travelSensors_test3.LATITUDE, travelSensors_test3.LONGITUDE

print ""
# Test for Summary data model
summmary_test = db_session.query(Summary).count()
print "Summary table entries =", summmary_test

# Use \ at the end for a line break.
summmary_test1 = db_session.query(Summary.Avg_Travel_Time, Summary.Destination) \
    .filter_by(Time=120).filter_by(Origin='51st_mueller').all()
for test in summmary_test1:
    print test.Avg_Travel_Time
