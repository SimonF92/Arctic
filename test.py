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





def plot_simb(simb_df, surface_distance, bottom_distance, timestamp, initial_snow_depth, distance_between_rangefinders):

    #calculate height of surface rangefinder above the ice surface
    height_above_ice = surface_distance[0] + initial_snow_depth

    #create arrays that store values for each timestamp
    snow_height = height_above_ice - surface_distance
    ice_thickness = distance_between_rangefinders - height_above_ice - bottom_distance
    #ice_thickness = - ice_thickness #make negative for plotting because it's below waterline

    #define temperature string position (height above ice)
    temp_string_length = 3.84 #standard SIMB3 temperature string has 2 cm spacing and 192 thermistors
    temp_string_offset = 0 #the axial distance between the surface rangefinder and the first thermister on the DTC
    temp_string_top = height_above_ice - temp_string_offset #distance from the top of the ice to the first thermistor in the temperature string
    temp_string_bottom = temp_string_length - temp_string_top
    temp_string_bottom = temp_string_bottom * (-1) #make negative for plotting
    

    #shift excel serial date (1900 epoch) to the Python 1970 epoch by adding the number of days between 01/01/1900 and 01/01/1970 
    #then subtract 1 to account for the famous 1900 excel leap year timestamp bug
    #timestamp = timestamp - 25568 - 1 
    simb_df['time_stamp']=simb_df['time_stamp'].round(0)
    simb_df['date']=pd.TimedeltaIndex(simb_df['time_stamp'],unit='d')+pd.to_datetime('1900-01-01')
    
    
    
    fig, ax = plt.subplots(figsize=(50,30))
    
    lons=simb_df['longitude'].values.tolist()
    centre_lon=np.mean(lons)
    
    
    lats=simb_df['latitude'].values.tolist()
    centre_lat=np.mean(lats)
    
    zoom=2
    
    m = Basemap(projection='stere',lat_0=centre_lat, lon_0=centre_lon,  lat_ts=centre_lat,resolution='l', width=2000000/zoom, height=1500000/zoom,ax=ax)
    x, y = m(lons,lats)

    m.fillcontinents(color='gray',lake_color='gray')
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='white')


    #c=df['Ts'].values.tolist()
    c=simb_df['air_temp'].values.tolist()
    #c=ice_thickness

    cs=m.scatter(x,y,80,c=c,ax=ax,cmap='jet')
    
    
    
    #ice_thickness=simb_df['bottom_distance']
    
    
    x2,y2=m(simb_df['longitude'].values.tolist(),simb_df['latitude'].values.tolist())

    c2=simb_df['date'].dt.date.tolist()
    c3=ice_thickness
    
    date_and_thickness=[]
    count=0
    
    for date,ice in zip(c2,c3):
        full=(str(date)+ ' ' + str(ice.round(2)) + 'm')
        
        date_and_thickness.append(full)
       
        
    


    texts = []
    date=0



    for (x,y, label) in zip(x2, y2, date_and_thickness):
        if date%90 == 0 or date ==0:        
        
            if label == str:
                t=ax.text(x, y, label,color='red', ha='center', size=120,
                 bbox=dict(boxstyle="round", facecolor='wheat'))
                texts.append(t)
            else:
                t=ax.text(x, y, label,color='black', ha='center', size=30,
                 bbox=dict(boxstyle="round", facecolor='lightgrey' ))
                texts.append(t)
            
        else:
            pass
            
        date+=1

    #texts.append(ax.text(-81, -180, d1, size=20))


    adjust_text(texts, ax=ax, precision=0.001,
    expand_text=(2.01, 2.05), expand_points=(2.01, 2.05),
    force_text=(0.01, 0.25), force_points=(0.01, 0.25),
    arrowprops=dict(arrowstyle='-', color='gray', alpha=.8),ha='right')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    cbar=plt.colorbar(cs,shrink=0.5,ax=ax)
    cbar.set_label("Buoy Temperature Read-out (degC)",size=30)
    cbar.ax.tick_params(labelsize=25) 


    

    plt.show()

    
    


def plot_from_csv(path_to_data: str, initial_snow_depth: float, plot_range):

    #try to read csv at input location
    try:
        simb_df = pd.read_csv(path_to_data,skiprows=plot_range[0], nrows=plot_range[1]) 
        #simb_df=simb_df.tail(-5)#create pandas dataframe from csv
        simb_df=simb_df[simb_df['wdt_counter']>1]
        
        timestamp = simb_df.time_stamp.to_numpy()       #extracts time stamp from simb_df dataframe, converts to numpy array
    except FileNotFoundError:
        print('Invalid Path, please check file location.')
        return

    # Create plot from input

    # Distance between sounders in meters, used for bounding the Ice Mass Balance Plot
    sounder_dist = 4.05

    # Extract relevant data from dataframe, convert to numpy array
    snow_dist = simb_df.surface_distance.to_numpy()                     # distance from upper sounder to snow
    water_depth = simb_df.bottom_distance.to_numpy()                    # distance from lower sounder to bottom of ice
    dtc_values = simb_df.filter(like='dtc_values_').to_numpy().T        # temperature string data at 2 cm intervals

    # Call plot function for ice mass balance plot
    plot_simb(simb_df, snow_dist, water_depth, timestamp, initial_snow_depth, sounder_dist)
    
    
plot_from_csv('https://app.cryosphereinnovation.com/sbd_data/SIMB3_859790.csv',0.2,[0, 3378])
