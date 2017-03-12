from context import Base, TravelSensor, Summary

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine
import numpy as np
import csv
import matplotlib.pyplot as plt
import math as m

# Configuration
engine = create_engine('sqlite:///../database.db')
Base.metadata.create_all(bind=engine)

# Create a new database session
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Database model definition:

# class TravelSensor(Base):
#     __tablename__ = 'TravelSensor'
#
#     READER_ID = Column(String(250), nullable=False)
#     ATD_SENSOR_ID = Column(Integer, primary_key=True)
#     PRIMARY_ST_SEGMENT_ID = Column(Integer, nullable=False)
#     SIGNAL_ENG_AREA = Column(String(250), nullable=False)
#     LOCATION_NAME = Column(String(250), nullable=False)
#     PRIMARY_ST = Column(String(250), nullable=False)
#     CROSS_ST = Column(String(250), nullable=False)
#     LATITUDE = Column(Float, nullable=False)
#     LONGITUDE = Column(Float, nullable=False)

# class Summary(Base):
#     __tablename__ = 'Summary'
#
#     index = Column(Integer, primary_key=True)
#     Avg_Travel_Time = Column(Float, nullable=False)
#     Destination = Column(String(250), nullable=False)
#     Origin = Column(String(250), nullable=False)
#     Sample_count = Column(Integer, nullable=False)
#     Time = Column(Integer, nullable=False)
#     Weekday = Column(Integer, nullable=False)
#     Year = Column(Integer, nullable=False)

# Test for TravelSensor data model
travelSensorsCount = db_session.query(TravelSensor).count()
print "Travel Sensor Entry Count:", travelSensorsCount

travelSensors_test1 = db_session.query(TravelSensor).all()
for sensor in travelSensors_test1:
    print sensor.READER_ID, sensor.LATITUDE, sensor.LONGITUDE

primary_st = "WILLIAM CANNON DR"
print ""
print "Travel Sensor with PRIMARY_ST =", primary_st
travelSensors_test2 = db_session.query(TravelSensor).filter_by(PRIMARY_ST=primary_st).all()
# If you use .all(), you will get a list of TravelSensor objects.
for sensor in travelSensors_test2:
    print sensor.READER_ID, sensor.LATITUDE, sensor.LONGITUDE

lat = 30.3
print ""
print "Fetch the first sensor with latitude greater than", lat
travelSensors_test3 = db_session.query(TravelSensor).filter(TravelSensor.LATITUDE > lat).first()
# Notice that if you use .first(), it will be an object and not a list.
print travelSensors_test3.READER_ID, travelSensors_test3.LATITUDE, travelSensors_test3.LONGITUDE

print ""
# Test for Summary data model
summmary_test = db_session.query(Summary).count()
print "Summary table entries =", summmary_test


#Use \ at the end for a line break.
#summmary_test1 = db_session.query(Summary.Avg_Travel_Time, Summary.Destination) \
#    .filter_by(Time=120).filter_by(Origin='51st_mueller').all()
#for test in summmary_test1:
#    print test.Destination, test.Avg_Travel_Time

summary_test2 = db_session.query(Summary.Avg_Travel_Time, Summary.Origin, Summary.Destination, Summary.Time) \
    .filter(Summary.Origin.contains('amar')).filter(Summary.Destination.contains('amar')).filter_by(Year=2016).filter_by(Weekday=0).all()
#for test in summary_test2:
#    print (test.Avg_Travel_Time, test.Origin, test.Destination)
Lamar = ['Parmer','Braker','Rundberg','Airport', 'Koenig','51st', '45th', '38th', '29th', '24th', 'mlk', '12th' ,'6th','5th', 'Riverside' ,'Barton_Springs', 'Lamar_Square',  'Oltorf','Blue_Bonnet', 'and_Manchca_Barton_skyway', 'BrodieOaks']
#Lamar = ['6th','5th']
traveltime=np.zeros((len(Lamar), 96))
samples = np.zeros((len(Lamar), 4*24))
average_traveltime = np.zeros((len(Lamar), 4*24))
lowest_traveltime =np.zeros((len(Lamar), 96))
percentage_traveltime=np.zeros((len(Lamar), 96))
var_traveltime = np.zeros((len(Lamar), 96))

print("traveltime")

for test in summary_test2:
    for i in range(len(Lamar)-1):
        #print test.Origin.strip("Lamar_"), Lamar[i]
        if ((test.Origin.lower()) ==("lamar_")+Lamar[i].lower()) and (test.Destination.lower()==('lamar_')+Lamar[i+1].lower()):
            print test.Origin, test.Destination, test.Avg_Travel_Time, test.Time
            traveltime[i][test.Time/15] += test.Avg_Travel_Time
            samples[i][test.Time/15] +=1
            if test.Avg_Travel_Time<lowest_traveltime[i][test.Time/15] or lowest_traveltime[i][test.Time/15] == 0:
                lowest_traveltime[i] = test.Avg_Travel_Time

#print traveltime[0][0], samples[0][0]


average_traveltime=traveltime/(samples+0.0001)
percentage_traveltime=average_traveltime/(lowest_traveltime+0.1)
Error=np.zeros(len(Lamar))

standard_deviation=np.std(average_traveltime, axis=1)

mean= avg=np.mean(average_traveltime, axis=1)

var_traveltime=(average_traveltime-mean)/standard_deviation


plt.xlim(0,95)
plt.ylim(0,19) #Or whateverplt.xlim(-30,80)

plt.imshow(var_traveltime, cmap='hot', interpolation= 'catrom')
plt.colorbar()
plt.show()

plt.imshow( average_traveltime, cmap='hot', interpolation= 'catrom')
plt.colorbar()
plt.show()

plt.imshow(percentage_traveltime, cmap='hot', interpolation= 'catrom')
plt.colorbar()
plt.show()

b=open('test.csv', 'w')
abc=csv.writer(b)
abc.writerows(average_traveltime)

b=open('test1.csv', 'w')
abc=csv.writer(b)
abc.writerows(var_traveltime)

