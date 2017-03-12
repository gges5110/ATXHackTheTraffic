import pandas as pd
import datetime
import numpy as np
path = "/Users/user/Downloads/Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv"

df = pd.read_csv(path,nrows=17508)

ts = df.timestamp
origin = df.origin_reader_identifier
destination = df.destination_reader_identifier
traveltime = df.average_travel_time_seconds

weekday = []
Month = []
ODpair = []
Year = []
for ii in range(len(ts)):
    ODpair.append(origin[ii]+'-'+destination[ii])
    month = ts[ii][0:2]
    day = ts[ii][3:5]
    year = ts[ii][6:10]
    d = datetime.datetime(int(year),int(month),int(day))
    weekday.append(str(d.isoweekday()))
    Year.append(year)

df2 = pd.DataFrame({'Year': Year, 'OD pair': ODpair,
                    'Month': month,'Travel time': traveltime})

meantime = df2.groupby(['OD pair','Year']).aggregate(np.mean)
time_std = df2.groupby(['OD pair','Year']).aggregate(np.std)
meantime['STD'] = time_std

#print (meantime)
print(Month)
#meantime.to_csv('traveltime_groupbyODYearMonth.csv')
#print('Done')