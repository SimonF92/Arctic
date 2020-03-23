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

buoys= {"https://data.meereisportal.de/download/buoys/2019T56_300234065176750_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TEMP_proc.csv",
     
       "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_TEMP_proc.csv",
  
       "https://data.meereisportal.de/download/buoys/2020T60_300234066299840_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2020T60_300234066299840_TEMP_proc.csv",

       "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_TEMP_proc.csv",
        
       #"https://data.meereisportal.de/download/buoys/2019T67_300234068704730_HEAT120_proc.csv":
        #"https://data.meereisportal.de/download/buoys/2019T67_300234068704730_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_TEMP_proc.csv",
        
       #"https://data.meereisportal.de/download/buoys/2019T69_300234068700320_HEAT120_proc.csv":
        #"https://data.meereisportal.de/download/buoys/2019T69_300234068700320_TEMP_proc.csv",
        
       "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_TEMP_proc.csv",
      
       "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_HEAT120_proc.csv":
        "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_TEMP_proc.csv"
      
      
      }

s=0
#iterates through individual buoys based on their HEAT and TEMP data
for buoy,temp_buoy in buoys.items():
    #this one reads HEAT, HEAT is used for the air_snow and snow_ice boundaries
    url=buoy
    df=pd.read_csv(url)
    
    
    #this one reads TEMP, TEMP is used for the ice_water boundary
    url2=temp_buoy
    dftemp=pd.read_csv(url2)
    #because TEMP takes 4x measurements against HEAT, TEMP must be reduced by 4x
    dftemp=dftemp.iloc[::4, :]
    #cuts out time,latitude and longitude for later dataframe, including T1 as requested
    time_thickness=dftemp.iloc[:,:4]
    

    #calculates length of dataframe
    x=len(df)
    #i is the value which allows the for loop to iterate through every line of the dataset to 
    #provide 6-hourly measurements
    i=(-1)
    
    
    #thicky is a list of ice thicknesses across the time series
    thicky=[]
    #snow is a list of snow thicknesses across the time series
    snowy=[]
    snow_air=[]
    ice_snow=[]
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
        #df2=df2.tail(100)
        df2.reset_index(level=0, inplace=True)
        
        #calculates the change in HEAT readings between adjacent thermistors
        df2["Temp_Change"]=df2.mean_t.diff()
        #redundant but left in
        df3= df2.where(df2.Temp_Change<-0.2)
        #calculates the thermal capacity of the "core" 100 thermistors which is the last 100 (those in water)
        dfthermalcore=df2.tail(100)
        #calculate the mean of these
        coretemp=dfthermalcore.mean_t.mean()
        #issues with measurements of the very bottom thermistor
        df2=df2.head(-5)
        #caculate the difference between thermistor and the "core"
        df2["Deltacore"]=df2.mean_t-coretemp
        #only keep thermistors which deviate largely from the "core", label as not_ice
        not_ice=df2.where(df2.Deltacore>0.7)
        not_ice=not_ice.dropna()
        #snow_ice is the bottomost of the not_ices
        snow_ice_boundary= not_ice.tail(1)
        x=list(snow_ice_boundary.index.values)
        x=int(x[0])
        #derive thermistor number
        snow_ice_thermistor=x
        
        ##########
        #new stuff!
        ##########
        
        df1=df.iloc[(i-10):i]
        dfs=df1.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
        #subset a dataframe as that not in ice by slicing at x, the value of the top of ice
        dfs=dfs.iloc[:,:x]
        dfb=dfs
        dfb = dfb.T.reset_index(drop=True).T
        #for each thermistor in this subset, calculate the differences between concurrent readings (air most variable)
        for column in dfb:
            dfb[column]=dfb[column].diff()
            #print(dfx[column])

        dfb=dfb.dropna()
        dfb
        #calculate mean and stdev
        dfb.loc['stdev'] = dfb.std()
        dfb.loc['mean_t'] = dfb.mean()
        dfb=dfb.tail(2)
        dfb=dfb.T
        #snow_air is therefore the point at which there is a sudden shift in stdev, can be seen properly here (d120 colour plot):
        #https://data.meereisportal.de/gallery/index_new.php?lang=en_US&active-tab1=method&active-tab2=buoy&singlemap&buoyname=2019T56
        dfsnow=dfb.where(dfb.stdev<0.1)
        dfsnow=dfsnow.dropna()
        #snow is the length of these thermistors
        snow=round(((len(dfsnow)*2)/100),3)
        snow_air_thermistor=x-(len(dfsnow))


        
        #subsets the dataframe for these consecutive 10*6hourly measurements
        dfx=dftemp.iloc[(i-10):i]
        #drop unwanted columns
        dfx=dfx.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
        
        #calculate stdev of every thermistor within this subsetted dataframe consisting of 10 measurements
        dfx.loc['stdev'] = dfx.std()
        #calculate mean temp of every therminstor within this subsetted dataframe consisting of 10 measurements
        dfx.loc['mean_t'] = dfx.mean()
        
        #subset dataframe again for only stdev at each thermistor  and mean temperature at each thermistor
        dfx=dfx.tail(2)
        dfy=dfx.T
        #df2=df2.tail(100)
        dfy.reset_index(level=0, inplace=True)
        y=len(dfy)
     
  
        #keep only values which are either in ice or water by subtracting (x)[thermistors] from
        # (y)[thermistors]
        ice_water=dfy.tail(y-x)
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
        z=list(ice_water_boundary.index.values)
        z=int(z[0])
        #therms becomes a simple list of the numbers for each relevant thermistor
        therms=list(ice.index.values)
        
        #ice thickness is therefore the number of these thermistors
        thickness=(len(therms)*2)/100
        #appends the original thicky list with these values
        thicky.append(thickness)
        ice_snow.append(x)
        snow_air.append(snow_air_thermistor)
        snowy.append(snow)
     

    #generic pandas dataframe work
    time_thickness=time_thickness.iloc[::-1]
    time_thickness=time_thickness.reset_index(drop=True)
    #thick from above then becomes the column of a dataframe
    thicky=pd.DataFrame((thicky),columns=["Thickness"])
    icea=pd.DataFrame((ice_snow),columns=["Ice_Snow_Thermistor"])
    icew=pd.DataFrame((snow_air),columns=["Snow_Air_Thermistor"])
    snowy=pd.DataFrame((snowy),columns=["SnowDepth"])
    #thicy and snowy are then added to the time_thickness dataframe which was made at the very start
    time_thickness = pd.concat([time_thickness,thicky],axis=1,sort=False)
    time_thickness = pd.concat([time_thickness,snowy],axis=1,sort=False)
    time_thickness = pd.concat([time_thickness,icea],axis=1,sort=False)
    time_thickness = pd.concat([time_thickness,icew],axis=1,sort=False)
    #generic pandas dataframe work
    time_thickness=time_thickness.iloc[::-1]
    time_thickness=time_thickness.reset_index(drop=True)
    time_thickness=time_thickness.dropna()
    
    #values for ice and snow display some variability and may be made more reliable by neighbours, 
    #use exponentially weighted mean calculation to smooth, based on nearest 20 neighbours
    time_thickness["Thickness [Smoothed] (m)"]=pd.Series.ewm(time_thickness["Thickness"],span=20).mean()
    time_thickness["Snow Depth [Smoothed] (m)"]=pd.Series.ewm(time_thickness["SnowDepth"],span=20).mean()
    
    buoy_ids=["T56","T58","T60","T62","T63","T64","T65","T66","T68","T70","T72"]

    #write individual time_thickness dataframes to their respective buoys in csv format
    buoy_id=buoy_ids[s]
    time_thickness["Buoy"]=buoy_id
    s+=1
    print("Processing Buoy: " +buoy_id)
    
    #time_thickness.to_csv("C:\\Users\\2087455F\\Desktop\\Final Python\\Buoys\\" + str(buoy_id) + "dT120_thickness_data.csv",index=False)
    
    if buoy_id=="T56":
        full_dataset=time_thickness
    else:
        full_dataset=full_dataset.append(time_thickness)
    #time_thickness=time_thickness.append(time_thickness, ignore_index=True)
full_dataset.to_csv("C:\\Users\\2087455F\\Desktop\\Final Python\\Buoys\\dT120_combined_thickness_data.csv",index=False)

