import pandas as pd
import datetime
import numpy as np
path = "/Users/user/Downloads/Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv"

df = pd.read_csv(path)

ts = df.timestamp
origin = df.origin_reader_identifier
destination = df.destination_reader_identifier
avg_speed = df.average_speed_mph

weekday = []
Month = []
ODpair = []
Year = []
Totalmin = np.ones(len(ts))
for ii in range(len(ts)):
    ODpair.append(origin[ii]+'-'+destination[ii])
    month = ts[ii][0:2]
    day = ts[ii][3:5]
    year = ts[ii][6:10]

    if ts[ii][20:22] == 'AM':
        hour = int(ts[ii][12:13])

    if ts[ii][20:22] == 'PM':
        hour = int(ts[ii][12:13]) + 12

    Totalmin[ii] = hour * 60 + int(ts[ii][15:16])
    d = datetime.datetime(int(year),int(month),int(day))
    weekday.append(str(d.isoweekday()))
    Year.append(year)

df2 = pd.DataFrame({'Year': Year, 'ODpair': ODpair,
                    'Month': month,'Average_speed_in_mile-hour': avg_speed,
                    'Weekday': weekday, 'Time_min': Totalmin})


df2.to_csv('TrimFile.csv')
print('Done')