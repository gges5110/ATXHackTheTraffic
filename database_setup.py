# Configuration
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# End of Configuration

# Class Summary
class Summary(Base):
    __tablename__ = 'Summary'

    Id = Column(Integer, primary_key=True, nullable=False)
    Avg_Travel_Time = Column(Float, nullable=False)
    Destination = Column(String(250), nullable=False)
    Origin = Column(String(250), nullable=False)
    Sample_count = Column(Integer, nullable=False)
    Time = Column(Integer, nullable=False)
    Weekday = Column(Integer, nullable=False)
    Year = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'Id': self.Id,
            'Avg_Travel_Time': self.Avg_Travel_Time,
            'Destination': self.Destination,
            'Origin': self.Origin,
            'Sample_count': self.Sample_count,
            'Time': self.Time,
            'Weekday': self.Weekday,
            'Year': self.Year
        }

# Class
class TravelSensor(Base):
    __tablename__ = 'TravelSensor'
    ID = Column(Integer, primary_key=True, nullable=False)
    READER_ID = Column(String(250), nullable=False)
    LATITUDE = Column(Float, nullable=False)
    LONGITUDE = Column(Float, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.ID,
            'reader_id': self.READER_ID,
            'latitude': self.LATITUDE,
            'longtitude': self.LONGITUDE
        }
