import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import animation
import ffmpeg


sns.set(font_scale=1.5)
sns.set_style("whitegrid")

plt.figure(figsize=(10,12))

url="https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TEMP_proc.csv"
df=pd.read_csv(url)
df

fig = plt.figure()
ax = Axes3D(fig)

#i=0

#while i<100

df1=df.tail(10)
df1.loc['stdev'] = df1.std()
df1.loc['mean_t'] = df1.mean()
df1

df1=df1.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
df1

df1=df1.tail(2)
df1

df2=df1.T
df2

df2["Change"]=df2.stdev.diff()
df2["Change_sq"]=df2["Change"]*df2["Change"]

df2.reset_index(level=0, inplace=True)


df2=df2.head(-1)
#df2=(df2["index"].str.rstrip('(degC)'))




#sort the data ranked by the magnitude of change in standard deviation between adjacent thermistors
df3= df2.sort_values(by='Change')
#select the "air to ice" boundary as the thermistor with the highest 
#change in stdev (as air transitions to something else)
air_ice_boundary= df3.head(1)
#calculate the number of thermistors
y=len(df2)
#get a raw value for the air_ice thermistor
x=list(air_ice_boundary.index.values)
x=int(x[0])
air_ice_thermistor=x
#keep only values which are either in ice or water by subtracting all thermistors in "air"
ice_water=df2.tail(y-x)
#take the bottom 10 thermistors to calculate water temp
corewater=ice_water.tail(10)
meanwater=corewater.mean_t.mean()
#subtract the temperatures of all ice or water thermistors from the water temp
ice_water["D"]=ice_water.mean_t-meanwater
#keep thermistors where the difference between water temp and thermistor is greater than -0.5C
ice=ice_water.where(ice_water.D<-0.5)
ice=ice.dropna()
#take the bottom-most of these thermistors as the "ice to water" boundary
ice_water_boundary=ice.tail(1)
#therms becomes a simple list of the numbers for each relevant thermistor
therms=list(ice.index.values)
#take the top-most of these thermistors as the "ice to air" thermistor
air_ice_thermistor=therms[0]
#take the bottom-most of these thermistors as the "ice to water" thermistor
ice_water_thermistor=therms[-1]
#each thermistor is 2cm apart, so calculate thickness based on this
thickness=2*(ice_water_thermistor-air_ice_thermistor)/100
#convert thickness to "words" with a unit
thickness_str=str(thickness) + "metres"

thickness_str

frames=[air_ice_boundary,ice_water_boundary]
coords=pd.concat(frames)

coords









fig.set_size_inches(7, 7, True)


ax.view_init(30, 140)

ax.scatter(df2.index,df2.mean_t, df2.Change, c = df2.mean_t,cmap="plasma", marker='o',s=10)
for x, y, z, label in zip(air_ice_boundary.index,air_ice_boundary.mean_t, air_ice_boundary.Change, air_ice_boundary["index"]):
        ax.text(x, y, z, label,size=20)
for x, y, z, label in zip(ice_water_boundary.index,ice_water_boundary.mean_t, ice_water_boundary.Change, ice_water_boundary["index"]):
        ax.text(x, y, z, label,size=20)
ax.text(60, -10, -0.3,thickness_str,size=30)

ax.plot(coords.index, coords.mean_t, coords.Change, linewidth=2,c="red")

#ax.plot(df2.index, df2.mean_t, df2.Change, linewidth=0.2,c="black")
ax.set_xlabel('Thermistor', fontsize=15, rotation=150)
ax.set_ylabel('Mean Temperature', fontsize=15)
ax.set_zlabel("60-hour Stdev Temp", fontsize=15)


g=fig


#g.savefig('C:\\Users\\2087455F\\Desktop\\Final Python\\3dbuoy.png', format="png")



def init():
    ax.scatter(df2.index,df2.mean_t, df2.Change, c = df2.mean_t,cmap="plasma", marker='o',s=10)
    ax.plot(df2.index, df2.mean_t, df2.Change, linewidth=0.2,c="black")
    ax.plot(coords.index, coords.mean_t, coords.Change, linewidth=2,c="red")
    for x, y, z, label in zip(air_ice_boundary.index,air_ice_boundary.mean_t, air_ice_boundary.Change, air_ice_boundary["index"]):
        ax.text(x, y, z, label,size=20)
    for x, y, z, label in zip(ice_water_boundary.index,ice_water_boundary.mean_t, ice_water_boundary.Change, ice_water_boundary["index"]):
        ax.text(x, y, z, label,size=20)
    ax.text(60, -10, -0.3,thickness_str,size=30)
    ax.plot(coords.index, coords.mean_t, coords.Change, linewidth=2,c="red")
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

fig.set_size_inches(7, 7, True)
# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
                               
                        
# Save
anim.save('C:\\Users\\2087455F\\Desktop\\Final Python\\3dbuoy_2.mp4', fps=30, dpi=200, extra_args=['-vcodec', 'libx264'])
