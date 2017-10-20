# ATXHackTheTraffic

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4a7ff1eb19fa47ec98984815942a20c0)](https://www.codacy.com/app/gges5110/ATXHackTheTraffic?utm_source=github.com&utm_medium=referral&utm_content=gges5110/ATXHackTheTraffic&utm_campaign=badger)

This is a project for travel time prediction in Austin, TX using the dataset provided by the City of Austin.

## Quick Overview
Make sure you have [Python 2.7](https://www.python.org/download/releases/2.7/) installed on your system.
### Install Dependencies
```
pip install -r requirements.txt
```

### Database Setup
1. Download Bluetooth Travel Sensor data from [City of Austin Website](https://data.austintexas.gov/Transportation-and-Mobility/Bluetooth-Travel-Sensors-Traffic-Match-Summary-Rec/v7zg-5jg9/data)
2. Put ```Travel_Sensors.csv``` and ```Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv``` in the project folder.

```sh
cd database_processing
python preprocess.py
```

### Start Server
```python
python run.py
```
Open http://localhost:8000/ to see the app running.

# Features
### Travel Time Prediction
Select the origin, destination and time to see how long it takes to get there.
![Image of travelTimePrediction](https://github.com/gges5110/ATXHackTheTraffic/blob/master/website_images/travelTimePrediction.png)

### History Stats
See the history stats for the average travelling time between each station.
![Image of historyStats](https://github.com/gges5110/ATXHackTheTraffic/blob/master/website_images/historyStats.png)

### Traffic Heat Map
Overview the traffic on Lamar Road based on different section and time.
![Image of trafficHeatMap](https://github.com/gges5110/ATXHackTheTraffic/blob/master/website_images/trafficHeatMap.png)

# Technical Details
### Server Routes
They are stored inside [views](https://github.com/gges5110/ATXHackTheTraffic/tree/master/views) folder. To add a new route, 
  1. Add a new .py file in views/ 
  2. Import it into run.py
  3. Register the blueprint to our app.

The new .py file should have a format like this:
```python
from flask import Blueprint

routeName = Blueprint('routeName', __name__)

@routeName.route("/routeName", methods=['GET'])
def routeName_function():
    return "The new route page."
```

### Tests
Tests are put in [tests](https://github.com/gges5110/ATXHackTheTraffic/tree/master/tests) folder. 
If you want to import something from the top level module, add it to [context.py](https://github.com/gges5110/ATXHackTheTraffic/blob/master/tests/context.py)
and then import to your test file.
