#
#
#concept and coding by SimonF92 and Uniquorn (Arctic Sea Ice Forum) @ https://forum.arctic-sea-ice.net/
#
#
#uncomment and run this first line if you get an error about not having pandas
#! pip install pandas



import pandas as pd

#
#
#
#the data from 3 of the buoys is bugged at the moment, I am looking into it, I think 57 and 59 are down

buoys= {"https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TEMP_proc.csv":"T56",
       #"https://data.meereisportal.de/download/buoys/2019T57_300234065177750_TEMP_proc.csv":"T57",
       "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_TEMP_proc.csv":"T58",
       #"https://data.meereisportal.de/download/buoys/2019T59_300234065170760_TEMP_proc.csv":"T59",
       "https://data.meereisportal.de/download/buoys/2020T60_300234066299840_TEMP_proc.csv":"T60",
       #"https://data.meereisportal.de/download/buoys/2020T61_300234065768480_TEMP_proc.csv":"T61",
       "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_TEMP_proc.csv":"T62",
       "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_TEMP_proc.csv":"T63",
       "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_TEMP_proc.csv":"T64",
       "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_TEMP_proc.csv":"T65",
       "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_TEMP_proc.csv":"T66",
       "https://data.meereisportal.de/download/buoys/2019T67_300234068704730_TEMP_proc.csv":"T67",
       "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_TEMP_proc.csv":"T68",
       "https://data.meereisportal.de/download/buoys/2019T69_300234068700320_TEMP_proc.csv":"T69",
       "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_TEMP_proc.csv":"T70",
       "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_TEMP_proc.csv":"T71",
       "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_TEMP_proc.csv":"T72"
      
      
      }

buoy_ids=[]
ice_thickness=[]

#iterates through individual buoys based on their link and buoy id
for buoy,buoy_id in buoys.items():
    url=buoy
    df=pd.read_csv(url)
    #cuts out time,latitude and longitude for later dataframe
    time_thickness=df.iloc[:,:3]
    

    #calculates length of dataframe
    x=len(df)
    #i is the value which allows the for loop to iterate through every line of the dataset to 
    #provide 6-hourly measurements
    i=(-1)
    #thicky is a list of ice thicknesses across the time series
    thicky=[]
    #snow is a list of snow thicknesses across the time series
    snowy=[]
    #for loop within this range fills each value in thicky and snowy based on the previous 10 6-hourly measuremnts
    for value in range (0,(x-10)):

        #subsets the dataframe for these consecutive 10*6hourly measurements
        df1=df.iloc[(i-10):i]
        #drop unwanted columns
        df1=df1.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
        #subtract 1 from i for every loop to allow iteration through time series
        i-=1
        #calculate stdev of every thermistor within this subsetted dataframe consisting of 10 measurements
        df1.loc['stdev'] = df1.std()
        #calculate mean temp of every therminstor within this subsetted dataframe consisting of 10 measurements
        df1.loc['mean_t'] = df1.mean()
        
        #subset dataframe again for only stdev at each thermistor  and mean temperature at each thermistor
        df1=df1.tail(2)
        df2=df1.T

        #calculate the change in stdev between adjacent thermistors, as thermally dynamic air/snow
        #transitions to thermally stable ice or sea water, "change" will be greatest
        df2["Change"]=df2.stdev.diff()
        #square this to provide positive values only (redundant)
        df2["Change_sq"]=df2["Change"]*df2["Change"]
        #reset index to help track cells
        df2.reset_index(level=0, inplace=True)
        #drop Nan of first measurement
        df2=df2.head(-1)

        #top 10 thermistors exist in air
        air=df2.head(10)
        #calculate mean air temp
        air_temp=air.mean_t.mean()
        #calculate change from air temp
        df2["Temp_Change"]=df2.mean_t-air_temp
        #calculate differences in "change from air temp" in adjacent thermistors
        df2["Temp_Change"]=df2.Temp_Change.diff()
        #square this to provide positive values
        df2["Temp_Change_sq"]=df2.Temp_Change*df2.Temp_Change
        #sort these values, the top thermistor here is the one closest to air as it has the smallest delta from
        #air temperature
        dfbareice= df2.sort_values(by="Temp_Change_sq",ascending=False)
        #select top thermistor as the boundary between air and ice, providing code does not detect snow
        air_ice_boundary=dfbareice.head(1)

        #calculate the mean change in standard deviation
        stdev_delta_mean=df2.Change.mean()
        #calculate the difference between mean and individual transistors
        df2["stdev_delta_mean"]=df2["Change"]-stdev_delta_mean
        #transistors which form stdev change dynamic region (looks like a U shape when plotted) 
        #are believed to be in snow
        dfU= df2.sort_values(by='stdev_delta_mean')
        #select the region wit large stdev snow
        dfU=dfU.where(dfU.stdev_delta_mean<-0.25)
        #reindex
        dfU.sort_index(inplace=True)
        #drop nan values
        dfU=dfU.dropna()
        #snow thickness is the length of these transistors
        snow=(len(dfU)*2)/100


        #calculate total number of transistors
        y=len(df2)
     

        #if the U-shaped region exists in the dataset, take the bottom-most of these transistors 
        #as the snow-ice boundary, and the snow-air boundary as the top most
        if len(dfU) > 0:
            snow_ice_boundary= dfU.tail(1)
            x=list(snow_ice_boundary.index.values)
            x=int(x[0])
            snow_ice_thermistor=x
            
            snow_air_boundary=dfU.head(1)
            z=list(snow_air_boundary.index.values)
            z=int(z[0])
            snow_air_thermistor=z
            
        #if the U-shaped region does not exist, use the air-ice boundary as descrbied 2-segments above
        else:
            x=list(air_ice_boundary.index.values)
            x=int(x[0])



  
        #keep only values which are either in ice or water by subtracting (x)[thermistors] from
        # (y)[thermistors]
        ice_water=df2.tail(y-x)
        #take the bottom 10 thermistors to calculate water temp
        corewater=ice_water.tail(10)
        meanwater=corewater.mean_t.mean()
        #subtract the temperatures of all ice or water thermistors from the water temp
        ice_water["D"]=ice_water.mean_t-meanwater
        #keep thermistors where the difference between water temp and thermistor is greater than -0.5C
        #these thermistors are in ice
        ice=ice_water.where(ice_water.D<-0.5)
        ice=ice.dropna()


        #take the bottom-most of these thermistors as the "ice to water" boundary
        ice_water_boundary=ice.tail(1)
        #therms becomes a simple list of the numbers for each relevant thermistor
        therms=list(ice.index.values)
        #ice thickness is therefore the number of these thermistors
        thickness=(len(therms)*2)/100
        #appends the original thicky list with these values
        thicky.append(thickness)
        #appends the original snowy list with the snow values
        snowy.append(snow)

    #generic pandas dataframe work
    time_thickness=time_thickness.iloc[::-1]
    time_thickness=time_thickness.reset_index(drop=True)
    #thick from above then becomes the column of a dataframe
    thicky=pd.DataFrame((thicky),columns=["Thickness"])
    #as does snowy
    snowy=pd.DataFrame((snowy),columns=["SnowDepth"])
    #thicy and snowy are then added to the time_thickness dataframe which was made at the very start
    time_thickness = pd.concat([time_thickness,thicky],axis=1,sort=False)
    time_thickness = pd.concat([time_thickness,snowy],axis=1,sort=False)
    #generic pandas dataframe work
    time_thickness=time_thickness.iloc[::-1]
    time_thickness=time_thickness.reset_index(drop=True)
    time_thickness=time_thickness.dropna()
    
    #values for ice and snow display some variability and may be made more reliable by neighbours, 
    #use exponentially weighted mean calculation to smooth, based on nearest 20 neighbours
    time_thickness["Thickness [Smoothed] (m)"]=pd.Series.ewm(time_thickness["Thickness"],span=20).mean()
    time_thickness["Snow Depth [Smoothed] (m)"]=pd.Series.ewm(time_thickness["SnowDepth"],span=20).mean()

    #write individual time_thickness dataframes to their respective buoys in csv format
    time_thickness["Buoy"]=str(buoy_id)
    time_thickness.to_csv("C:\\Users\\2087455F\\Desktop\\Final Python\\Buoys\\" + str(buoy_id) + "_thickness_data.csv",index=False)
    
    if buoy_id=="T56":
        full_dataset=time_thickness
    else:
        full_dataset=full_dataset.append(time_thickness)
    #time_thickness=time_thickness.append(time_thickness, ignore_index=True)
full_dataset.to_csv("C:\\Users\\2087455F\\Desktop\\Final Python\\Buoys\\combined_thickness_data.csv",index=False)