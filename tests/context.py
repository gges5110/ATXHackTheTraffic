import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# If the error occur: import error: 'No module named' does exist
# use the command: export PYTHONPATH='.'
from database_setup import Base, Summary, TravelSensor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_db():
    engine = create_engine('sqlite:///database.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()

if __name__ == '__main__':
    db_session = init_db()
    print "travel sensor.table:", TravelSensor.__table__

    travelSensorsCount = db_session.query(TravelSensor).count()
    print "Travel Sensor Entry Count:", travelSensorsCount
