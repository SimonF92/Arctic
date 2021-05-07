from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline  
import warnings
import matplotlib.cbook
import matplotlib.cm as cm
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
from adjustText import adjust_text
import pandas as pd
from datetime import date

today = date.today()
d1 = today.strftime("%d/%m/%Y")



html= 'https://iabp.apl.uw.edu/TABLES/ArcticTable.php'
df = pd.read_html(html)
df=df[0]

df = df[1:] 
df.columns = ['BuoyID','WMO','Year','Buoy Type','Owner','Logistics','Latest Report','Latitude','Longitude','BP','Ts','Ta','DATA']
df=df.dropna(subset=['Ts'])
df=df.where(df['Ts']>-60)
df=df.where(df['Ts']<10)
df=df.dropna(subset=['Ts'])



df2=df.where(df['Latitude']>70)
df2=df2.dropna(subset=['Latitude'])
df2


fig, ax = plt.subplots(figsize=(50,30))

m = Basemap(projection='npstere',boundinglat=55,lon_0=0,resolution='l',ax=ax)
x, y = m(df['Longitude'].values.tolist(),df['Latitude'].values.tolist())

m.fillcontinents(color='gray',lake_color='gray')
m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
m.drawmapboundary(fill_color='white')


c=df['Ts'].values.tolist()

cs=m.scatter(x,y,150,c,ax=ax)


x2,y2=m(df2['Longitude'].values.tolist(),df2['Latitude'].values.tolist())

c2=df2['Ts'].values.tolist()

texts = []



for (x,y, label) in zip(x2, y2, c2):
    if label > 0:
        t=ax.text(x, y, label,color='red', ha='center', size=12,
         bbox=dict(boxstyle="round", facecolor='wheat'))
        texts.append(t)
    else:
        t=ax.text(x, y, label,color='blue', ha='center', size=12,
         bbox=dict(boxstyle="round", facecolor='wheat' ))
        texts.append(t)
        
texts.append(ax.text(-81, -180, d1, size=20))


adjust_text(texts, ax=ax, precision=0.001,
expand_text=(2.01, 2.05), expand_points=(2.01, 2.05),
force_text=(0.01, 0.25), force_points=(0.01, 0.25),
arrowprops=dict(arrowstyle='-', color='gray', alpha=.5),ha='right')

cbar=plt.colorbar(cs,shrink=0.5,ax=ax)
cbar.set_label("Buoy Temperature Read-out (degC)",size=20)

ax.set_title('https://iabp.apl.uw.edu/maps_daily_table.html: Buoy Temps',size=20)


fig.savefig('C:/Users/Administrator/Desktop/test.png', facecolor='w',bbox_inches='tight')
