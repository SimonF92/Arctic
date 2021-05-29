# check clean install of basemap functions properly
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




def cast_to_map(simb_df):
    #create large map fig
    fig, ax = plt.subplots(figsize=(50,30))
    
    
       
    def create_map_centre():
        #list all lons and lats and create mean of both to generate map centre automatically
        lons=simb_df['longitude'].values.tolist()
        centre_lon=np.mean(lons)
        lats=simb_df['latitude'].values.tolist()
        centre_lat=np.mean(lats)
        
        return lons, lats, centre_lon, centre_lat
    
               
    
    def create_map_template():
        #added zoom variable so users can easily change zoom
        zoom=1
        #steric projection onto basemap, width and height are in metres
        m = Basemap(projection='stere',lat_0=centre_lat, lon_0=centre_lon,  lat_ts=centre_lat,resolution='l', width=2000000/zoom, height=1500000/zoom,ax=ax)
        x_values, y_values = m(lons,lats)
        #visual changes to basemap, draws coastlines and meridians,parralels onto mop at appropriate coords
        m.fillcontinents(color='gray',lake_color='gray')
        m.drawcoastlines()
        m.drawparallels(np.arange(-80.,81.,20.))
        m.drawmeridians(np.arange(-180.,181.,20.))
        m.drawmapboundary(fill_color='white')
       
        return m, x_values, y_values 
    
    
    def create_map_labels():
        
        
        
        #create list of buoy ids
        buoys_list=simb_df['buoy_id'].values.tolist()
        #get unique strings
        buoys= list(set(buoys_list))

        #empty list for append
        labels_df=[]

        for buoy in buoys:
            #subset dataframe to buoys
            cut = simb_df[simb_df['buoy_id']==buoy]
            #get deployment row and current row, add these to labels_df
            deployment_date= cut.head(1)
            current_date= cut.tail(1)
            labels_df.append(deployment_date)
            labels_df.append(current_date)
        #create df proper from this
        labels_df=pd.concat(labels_df)
        labels_df




        #list of buoy ids
        buoy_labels=labels_df['buoy_id'].values.tolist()
        #list of dates in datetime
        date_labels=labels_df['date'].dt.date.tolist()
        #list of ice thickness
        ice_thickness_labels=labels_df['ice_thickness'].values.tolist()
        
        #coprdinates for labels on map
        lons=labels_df['longitude'].values.tolist()
        lats=labels_df['latitude'].values.tolist()
        x_labels, y_labels=m(lons, lats)

        
        date_and_thickness_labels=[]
        #create list of labels using all of the above
        for buoyid,date,ice in zip(buoy_labels,date_labels,ice_thickness_labels):
            full_label=(buoyid + '\n' + str(date)+ '\n' + str(round(ice,2)) + 'm')
        
            date_and_thickness_labels.append(full_label)
            
        
        
        
        
    
        #send coords of labels and labels to plotter
        return x_labels, y_labels, date_and_thickness_labels
 


    def produce_final_figure():
        #can be changed to any of the numerical headers in dataframe, ice thicknes does not look great due to anomalous 
        #values skewing colourmap, was considering smoothing data but is frowned upon unless valid
        colours=simb_df['air_temp'].values.tolist()
    
    
    
    
    
        #final figure is actually matplotlib scatter but underlay is map
        final_figure=m.scatter(x_values, y_values,100,c=colours,ax=ax,cmap='jet')
    
        final_figure_labels=[]
        #add labels using coords and labels, change properties to look good, alpha particularly useful
        for (x,y, label) in zip(x_labels, y_labels, date_and_thickness_labels):

            t=ax.text(x, y, label,color='black', ha='center', size=25,
             bbox=dict(boxstyle="round", facecolor='lightgrey', alpha=0.5 ))
            
            final_figure_labels.append(t)

        #use adjust text library to prevent bumping and overlap, add arrows for cosmetic reasons
        adjust_text(final_figure_labels, ax=ax, precision=0.001,
        expand_text=(2.01, 2.05), expand_points=(2.01, 2.05),
        force_text=(0.01, 0.25), force_points=(0.01, 0.25),
        arrowprops=dict(arrowstyle='-', color='gray', lw=5, alpha=.8),ha='right')
    
        #add colourbar for colours variable
        cbar=plt.colorbar(final_figure,shrink=0.5,ax=ax)
        #possible way to automatically update label using df.columns but didnt want to overcomplicate for users
        cbar.set_label("Air Temperature (degC)",size=30)
        cbar.ax.tick_params(labelsize=25) 
        
        return fig
    
    

    #call all functions
    lons, lats, centre_lon, centre_lat= create_map_centre()
    m, x_values, y_values = create_map_template()
    x_labels, y_labels, date_and_thickness_labels = create_map_labels()
    fig= produce_final_figure()
    
    plt.savefig('ap_test_map.png')
    plt.show()
    

    
    
    


def fetch_and_map_data():

    #can add any url or just use one
    urls=['https://app.cryosphereinnovation.com/sbd_data/SIMB3_443910.csv',
         #'https://app.cryosphereinnovation.com/sbd_data/SIMB3_859790.csv',
         'https://app.cryosphereinnovation.com/sbd_data/SIMB3_441910.csv']
    
    
    frames=[]
    #gets separate dataframes but will eventually concatenate
    for url in urls:
        
        
        print(url)
        try:

            simb_df = pd.read_csv(url) 
            buoy_id= url.split('/')[-1].rstrip('.csv')
            #for some reason wdt counter < 2 provides bugged data
            simb_df=simb_df[simb_df['wdt_counter']>2]
            simb_df['buoy_id']=buoy_id
        
        #copied following from previous tutorial
        except invalid_link:
            print('Invalid link, please check link address (right click on "download csv" and copy link')

        initial_snow_depth=0.2
        initial_surface_distance=simb_df['surface_distance'].values.tolist()[0]


        height_above_ice = initial_surface_distance + initial_snow_depth


        simb_df['snow_depth']=height_above_ice - simb_df['surface_distance'] 
        simb_df['ice_thickness']= 4.05- height_above_ice - simb_df['bottom_distance']

        #get dates, is a little different from previous tutorial
        simb_df['time_stamp']=simb_df['time_stamp'].round(0)
        simb_df['date']=pd.TimedeltaIndex(simb_df['time_stamp'],unit='d')+pd.to_datetime('1900-01-01')
        
        frames.append(simb_df)

        
    #cats all different buoys together   
    simb_df_full=pd.concat(frames,ignore_index=True)

    
    cast_to_map(simb_df_full)

fetch_and_map_data()
