# Configuration
# import os
# import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Base

engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)
db_session = scoped_session(sessionmaker(bind=engine))
