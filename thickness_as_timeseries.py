import pandas as pd


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


url="https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TEMP_proc.csv"
df=pd.read_csv(url)
time_thickness=df.iloc[:,:3]
time_thickness

x=len(df)
i=(-1)
thicky=[]

for value in range (0,(x-10)):


    df1=df.iloc[(i-10):i]
    df1=df1.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
    i-=1
    
    df1.loc['stdev'] = df1.std()
    df1.loc['mean_t'] = df1.mean()
    #df1=df1.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
    df1=df1.tail(2)
    df2=df1.T


    df2["Change"]=df2.stdev.diff()
    df2["Change_sq"]=df2["Change"]*df2["Change"]
    df2.reset_index(level=0, inplace=True)
    df2=df2.head(-1)

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
    ###air_ice_thermistor=therms[0]
    #take the bottom-most of these thermistors as the "ice to water" thermistor
    ###ice_water_thermistor=therms[-1]
    #each thermistor is 2cm apart, so calculate thickness based on this
    ###thickness=round((2*(ice_water_thermistor-air_ice_thermistor)/100),3)
    #convert thickness to "words" with a unit
    ###thickness_str=str(thickness) + " metres"
    
    thickness=(len(therms)*2)/100
       
    thicky.append(thickness)
    
    
    

#print(thicky)
time_thickness=time_thickness.iloc[::-1]
time_thickness=time_thickness.reset_index(drop=True)
thicky=pd.DataFrame((thicky),columns=["Thickness (m)"])

time_thickness = pd.concat([time_thickness,thicky],axis=1,sort=False)
time_thickness=time_thickness.iloc[::-1]
time_thickness=time_thickness.reset_index(drop=True)

time_thickness

#Change this to a directory of your choice, use \\ for windows and not \
time_thickness.to_csv("C:\\Users\\2087455F\\Desktop\\Final Python\\time_series_thickness.csv",index=False)
time_thickness

