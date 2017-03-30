# Configuration
# import os
# import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Base, User, Summary, TravelSensor, Catalog

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(bind=engine)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
