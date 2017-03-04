# Configuration
import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# End of Configuration

# Class
class User(Base):
    # Table
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'picture' : self.picture
        }

# Class Summary
class Summary(Base):
    __tablename__ = 'Summary'

    ID = Column(Integer, primary_key=True)
    AVG_TRAVEL_TIME = Column(Float, nullable=False)
    DESTINATION = Column(String(250), nullable=False)
    ORIGIN = Column(String(250), nullable=False)
    SAMPLE_COUNT = Column(Integer, nullable=False)
    TIME = Column(DateTime, nullable=False)
    WEEKDAY = Column(Integer, nullable=False)
    YEAR = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'ID': self.ID,
            'AVG_TRAVEL_TIME': self.AVG_TRAVEL_TIME,
            'DESTINATION': self.DESTINATION,
            'ORIGIN': self.ORIGIN,
            'SAMPLE_COUNT': self.SAMPLE_COUNT,
            'TIME': self.TIME,
            'WEEKDAY': self.WEEKDAY,
            'YEAR': self.YEAR
        }

# Class
class TravelSensor(Base):
    __tablename__ = 'TravelSensor'

    READER_ID = Column(String(250), nullable=False)
    ATD_SENSOR_ID = Column(Integer, primary_key=True)
    PRIMARY_ST_SEGMENT_ID = Column(Integer, nullable=False)
    SIGNAL_ENG_AREA = Column(String(250), nullable=False)
    LOCATION_NAME = Column(String(250), nullable=False)
    PRIMARY_ST = Column(String(250), nullable=False)
    CROSS_ST = Column(String(250), nullable=False)
    LATITUDE = Column(Float, nullable=False)
    LONGITUDE = Column(Float, nullable=False)

    @property
    def serialize(self):
        return {
            'reader_id': self.READER_ID,
            'atd_sensor_id': self.ATD_SENSOR_ID,
            'primary_st_segment_id': self.PRIMARY_ST_SEGMENT_ID,
            'signal_eng_area': self.SIGNAL_ENG_AREA,
            'location_name': self.LOCATION_NAME,
            'primary_st': self.PRIMARY_ST,
            'cross_st': self.CROSS_ST,
            'latitude': self.LATITUDE,
            'longtitude': self.LONGITUDE
        }

# Class
class Catalog(Base):
    # Table
    __tablename__ = 'catalog'

    # Mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }

# Configuration
engine = create_engine('sqlite:///database1.db')
Base.metadata.create_all(engine)
# End of Configuration
