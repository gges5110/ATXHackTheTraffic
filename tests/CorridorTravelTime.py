from context import Base, TravelSensor, Summary

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy import create_engine
import numpy as np
import csv
import matplotlib.pyplot as plt
import FindRoadConnectToCorridor

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

Corridor_name = 'lamar'

# Import relevant TravelSensor data
travelSensors = db_session.query(TravelSensor).filter(TravelSensor.READER_ID.contains(Corridor_name)).all()

# Import relevant Summary data
data_summary= db_session.query(Summary.Avg_Travel_Time, Summary.Origin, Summary.Destination, Summary.Time) \
.filter(Summary.Origin.contains(Corridor_name)).filter(Summary.Destination.contains(Corridor_name)).filter_by(Year=2016).filter_by(Weekday=0).all()

roads_connected_to_corridor = FindRoadConnectToCorridor(travelSensors)

Lamar = ['Parmer','Braker','Rundberg','Airport', 'Koenig','51st', '45th', '38th', '29th', '24th', 'mlk', '12th' ,'6th','5th', 'Riverside' ,'Barton_Springs', 'Lamar_Square',  'Oltorf','Blue_Bonnet', 'and_Manchca_Barton_skyway', 'BrodieOaks']

traveltime=np.zeros((len(Lamar), 96))
samples = np.zeros((len(Lamar), 4*24))
average_traveltime = np.zeros((len(Lamar), 4*24))
lowest_traveltime =np.zeros((len(Lamar), 96))
percentage_traveltime=np.zeros((len(Lamar), 96))
var_traveltime = np.zeros((len(Lamar), 96))

print("traveltime")

for test in data_summary:
    for i in range(len(Lamar)-1):
        #print test.Origin.strip("Lamar_"), Lamar[i]
        if ((test.Origin.lower()) ==(Corridor_name + "_")+Lamar[i].lower()) and (test.Destination.lower()==(Corridor_name + '_')+Lamar[i+1].lower()):
            print test.Origin, test.Destination, test.Avg_Travel_Time, test.Time
            traveltime[i][test.Time/15] += test.Avg_Travel_Time
            samples[i][test.Time/15] +=1
            if test.Avg_Travel_Time<lowest_traveltime[i][test.Time/15] or lowest_traveltime[i][test.Time/15] == 0:
                lowest_traveltime[i] = test.Avg_Travel_Time

#print traveltime[0][0], samples[0][0]


average_traveltime = traveltime/(samples+0.0001)
percentage_traveltime = average_traveltime/(lowest_traveltime+0.1)
Error=np.zeros(len(Lamar))

standard_deviation=np.std(average_traveltime, axis=1)
standard_deviation_rep = np.tile(standard_deviation, (96,1)).transpose()

mean = np.mean(average_traveltime, axis=1)
mean_rep = np.tile(mean, (96,1)).transpose()

zscore_traveltime = (average_traveltime-mean_rep)/standard_deviation_rep


plt.xlim(0,95)
plt.ylim(0,19) #Or whateverplt.xlim(-30,80)

plt.imshow(zscore_traveltime, cmap='hot', interpolation= 'catrom')
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