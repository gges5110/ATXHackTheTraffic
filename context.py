import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# If the error occur: import error: 'No module named' does exist
# use the command: export PYTHONPATH='.'
from database_setup import Base, TravelSensor, Summary, db_session
