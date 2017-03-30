import pandas as pd
import datetime
import numpy as np
path = "/Users/user/Downloads/Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv"

df = pd.read_csv(path, nrows = 5)

ts = df.timestamp
origin = df.origin_reader_identifier
destination = df.destination_reader_identifier
traveltime = df.average_travel_time_seconds
weekday = np.ones(len(ts))
for ii in range(len(ts)):
    month = ts[ii][0:2]
    day = ts[ii][3:5]
    year = ts[ii][6:10]
    d = datetime.datetime(int(year),int(month),int(day))
    weekday[ii] = str(d.isoweekday())

print(traveltime)
df2 = pd.DataFrame({'timestamp': ts, 'WeekDay': weekday})
print(df2)

# print (df.head())

# columns_names = df.columns.values;

# print (columns_names)

# print (df.describe())