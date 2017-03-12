import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
path = "/Users/user/Desktop/ATXHackTheTraffic/traveltime_groupbyODYearMonth.csv"

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Taxis, Yaxis = np.meshgrid(taxis, yaxis)
ax.plot_surface(Taxis, Yaxis, Matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()


