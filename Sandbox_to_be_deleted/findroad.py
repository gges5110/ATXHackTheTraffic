import pandas as pd
import datetime
import numpy as np
import csv
import matplotlib.pyplot as plt


path = "/Users/user/Downloads/Bluetooth_Travel_Sensors_-Traffic_Match_Summary_Records__TMSR_.csv"


df = pd.read_csv(path,nrows=10000000)


print('finish import')

ts = df.timestamp
origin = df.origin_reader_identifier
origin = origin.str.lower()
destination = df.destination_reader_identifier
destination = destination.str.lower()
avgspeed = df.average_speed_mph

road = ['lamar_parmer','lamar_braker','lamar_rundberg','lamar_payton_gin', 'lamar_morrow', 'lamar_airport', 'lamar_koenig','lamar_51st', 'lamar_45th', 'lamar_38th', 'lamar_29th', 'lamar_24th', 'lamar_mlk', 'lamar_12th' ,'lamar_6th','lamar_5th', 'lamar_riverside' ,'lamar_barton_springs', 'lamar_lamar_square', 'kinney_lamar', 'lamar_oltorf','lamar_blue_bonnet', 'lamar_and_manchca_barton_skyway', 'lamar_panther' ,'lamar_brodieoaks']

weekday = []
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
        hour = int(ts[ii][12:13])+12

    Totalmin[ii] = hour*60+int(ts[ii][14:16])
    d = datetime.datetime(int(year),int(month),int(day))
    weekday.append(str(d.isoweekday()))
    Year.append(year)

print('finish preprocessing')

roadpair=[]
for ss in range(len(road)-1):
    roadpair.append(road[ss]+'-'+road[ss+1])


df2 = pd.DataFrame({'ODpair': ODpair, 'AveSpeed': avgspeed,'Totalmin': Totalmin})
df2 = df2.groupby(['ODpair','Totalmin'],as_index=False).aggregate(np.mean)

df3 = df2[df2['ODpair'].isin(roadpair)]

taxis = np.linspace(0,24*60-15,(24*60-15)/15+1)
yaxis = np.linspace(0,len(roadpair),len(roadpair)+1)
Matrix = np.zeros(len(taxis)*len(yaxis)).reshape(len(yaxis),len(taxis))
odpair = df3.ODpair
for ii in range(len(roadpair)):
    include = odpair == roadpair[ii]

    if sum(include) > 0:
        speed = df3.AveSpeed[include]
        ind = speed.index
        time = df3.Totalmin[include]
        print(len(ind))
        for tt in range(len(ind)):
            Matrix[ii,taxis == time[ind[tt]]] = speed[ind[tt]]

fig = plt.figure(1,(8.,4.))
plt.imshow(Matrix,vmin = 0,vmax = 40)
plt.colorbar()
plt.show()

b = open('test.csv', 'w')
abc = csv.writer(b)
abc.writerows(Matrix)
b.close
print('Done')