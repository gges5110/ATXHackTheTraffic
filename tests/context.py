import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# If the error occur: import error: 'No module named' does exist
# use the command: export PYTHONPATH='.'
from database_setup import Base, TravelSensor, Summary
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

# Configuration
def init_db():
    engine = create_engine('sqlite:///../database.db')
    Base.metadata.create_all(bind=engine)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    return db_session
# End of Configuration
