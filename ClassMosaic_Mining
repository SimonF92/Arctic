import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import os

buoy_dir= "Buoy_Data"
if not 'workbookDir' in globals():
    workbookDir = os.getcwd()

path = os.path.join(workbookDir, buoy_dir)
if not os.path.exists(path):
    os.mkdir(path) 


class Buoy:
    def __init__(self, buoyid, temp, heat, loc, startdate):
        self.buoyid=buoyid
        self.temp=temp
        self.heat=heat
        self.loc=loc
        self.startdate=startdate
        
    def processbuoy(self):
        url_HEAT=self.heat
        df_HEAT_main=pd.read_csv(url_HEAT)

        url_TS=self.loc
        df_TS=pd.read_csv(url_TS)
        df_TS["Date"] = df_TS["time"].str[:10]
        #df_TS.drop_duplicates(subset ="date", keep = "first", inplace = True) 
        df_TS.columns=["ts_time","ts_latitude (deg)","ts_longitude (deg)","Date"]

        url_TEMP=self.temp
        df_TEMP=pd.read_csv(url_TEMP)
        df_TEMP=df_TEMP.iloc[::4, :]

        time_thickness=df_TEMP.iloc[:,:4]
        time_thickness["date"] = time_thickness["time"].str[:10]

        #time_thickness=df_TS.merge(time_thickness, left_on="date", right_on="date")
        #time_thickness=time_thickness.drop(["time", "latitude (deg)","longitude (deg)"], axis=1)
        names= ["Time","Latitude","Longitude","Air_Temp_(C)","Date"]  
        time_thickness.columns=names
        time_thickness["Time"] = time_thickness["Time"].str[11:]
        #time_thickness=time_thickness[["Date","Time","Latitude","Longitude","Air_Temp_(C)"]]




        number_of_days=len(df_HEAT_main)


        daily_ice_thickness=[]
        daily_snow_thickness=[]
        daily_Th_snow=[]
        daily_Th_ice=[]
        daily_Th_ocean=[]
        plots=[]


        i=(-1)

        for value in range (0,(number_of_days-10)):



            df_HEAT=df_HEAT_main.iloc[(i-10):i]
            df_HEAT=df_HEAT.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)        
            df_HEAT.loc['stdev'] = df_HEAT.std()
            df_HEAT.loc['mean_t'] = df_HEAT.mean()        
            df_HEAT=df_HEAT.tail(2)
            df_HEAT=df_HEAT.T
            df_HEAT.reset_index(level=0, inplace=True)
            df_HEAT["Temp_Change"]=df_HEAT.mean_t.diff()
            df_ocean=df_HEAT.tail(50)
            core_temperature=df_ocean.mean_t.mean()
            df_HEAT=df_HEAT.head(-5)
            df_HEAT["Deltacore"]=df_HEAT.mean_t-core_temperature
            thermistors_not_in_ice=df_HEAT.where(df_HEAT.Deltacore>1)
            thermistors_not_in_ice=thermistors_not_in_ice.dropna()
            Th_ice= thermistors_not_in_ice.tail(1)
            Th_ice=list(Th_ice.index.values)
            Th_ice=int(Th_ice[0])


            daily_Th_ice.append(Th_ice)



            df_HEAT=df_HEAT_main[(i-50):i]
            df_HEAT=df_HEAT.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
            df_HEAT=df_HEAT.iloc[:,:Th_ice]
            df_HEAT = df_HEAT.reset_index(drop=True)
            df_HEAT.loc['stdev'] = df_HEAT.std()
            df_HEAT=df_HEAT.tail(1)
            df_HEAT=df_HEAT.T
            thermistors_in_snow=df_HEAT.where(df_HEAT.stdev<0.05)
            thermistors_in_snow=thermistors_in_snow.dropna()
            snow_depth=round(((len(thermistors_in_snow)*2)/100),3)
            Th_snow=Th_ice-(len(thermistors_in_snow))



            daily_Th_snow.append(Th_snow)
            daily_snow_thickness.append(snow_depth)





            df_TEMP_subset=df_TEMP.iloc[(i-10):i]
            df_TEMP_subset=df_TEMP_subset.drop(['time', 'latitude (deg)','longitude (deg)'], axis=1)
            df_TEMP_subset.loc['stdev'] = df_TEMP_subset.std()
            df_TEMP_subset.loc['mean_t'] = df_TEMP_subset.mean()
            df_TEMP_subset=df_TEMP_subset.tail(2)
            df_TEMP_subset=df_TEMP_subset.T
            df_TEMP_subset.reset_index(level=0, inplace=True)
            total_thermistors_in_column=len(df_TEMP_subset)
            ice_or_water_thermistors=df_TEMP_subset.tail(total_thermistors_in_column-Th_ice)
            ice_thermistors=ice_or_water_thermistors.where(ice_or_water_thermistors.mean_t<-2.5)
            ice_thermistors=ice_thermistors.dropna()
            Th_ocean=ice_thermistors.tail(2)
            Th_ocean=list(Th_ocean.index.values)
            Th_ocean=int(Th_ocean[0])
            ice_thickness=list(ice_thermistors.index.values)
            ice_thickness=(len(ice_thickness)*2)/100



            daily_Th_ocean.append(Th_ocean)
            daily_ice_thickness.append(ice_thickness)




            i-=1



        time_thickness=time_thickness.iloc[::-1]
        time_thickness=time_thickness.reset_index(drop=True)

        Ice_Thickness=pd.DataFrame((daily_ice_thickness),columns=["Ice_Thickness_(m)"])
        Snow_Thickness=pd.DataFrame((daily_snow_thickness),columns=["Snow_Thickness_(m)"])                               
        Th_snow=pd.DataFrame((daily_Th_snow),columns=["Th(snow)"])                            
        Th_ice=pd.DataFrame((daily_Th_ice),columns=["Th(ice)"])   
        Th_ocean=pd.DataFrame((daily_Th_ocean),columns=["Th(ocean)"])

        variables= [Ice_Thickness,Snow_Thickness,Th_snow,Th_ice,Th_ocean]                                   
        for variable in variables:

            time_thickness = pd.concat([time_thickness,variable],axis=1,sort=False)

        time_thickness=time_thickness.dropna()    
        time_thickness=time_thickness.iloc[::-1]
        time_thickness=time_thickness.reset_index(drop=True)
        time_thickness=time_thickness.dropna()        
        time_thickness=time_thickness.sort_values(by=["Date"])

        loc=time_thickness.loc[time_thickness["Date"]==self.startdate].index[0]
        time_thickness=time_thickness.iloc[loc:]
        time_thickness["Change_in_Thickness_(m)"]= time_thickness["Ice_Thickness_(m)"].diff()


        
        buoy_id=self.buoyid
        time_thickness["Buoy"]=buoy_id
        #time_thickness= pd.DataFrame(np.repeat(time_thickness.values,12,axis=0))
        #newdf = pd.DataFrame(np.repeat(df.values,3,axis=0))

        time_thickness=pd.merge(df_TS,time_thickness,on="Date")


        time_thickness["Ice_Board"]=0
        time_thickness["Ice_Bottom"]=0-time_thickness["Ice_Thickness_(m)"]
        time_thickness["Snow"]=0+time_thickness["Snow_Thickness_(m)"]
        
        fig = plt.figure(figsize=(12,6))
        
        ax1 = fig.add_subplot(1, 1, 1)  


        plt.plot(time_thickness.Date, time_thickness.Ice_Bottom)
        plt.plot(time_thickness.Date, time_thickness.Snow,color="grey")

        plt.fill_between(time_thickness.Date,time_thickness.Ice_Bottom,-3,color="navy")
        plt.fill_between(time_thickness.Date,0,time_thickness.Ice_Bottom,color="azure")

        time_thickness_drops=time_thickness.drop_duplicates(subset =["Date"], keep = "first")
        datelen=time_thickness_drops.Date.tolist()
        datelenfull=time_thickness.Date.tolist()

        #ax1.set(xticks=np.arange(min(x), max(x)+1, 1.0))

        #ax1.set(xticks=[0,20, 40, 60, 80, 100, 120, 140])
        ax1.set(xticks=range(0, len(datelen), 10))
        ax1.set_ylabel("Delta (Metres)",fontsize=15)
        plt.xticks(rotation=45)
        plt.ylim([-2.5, 1])
        #plt.xlim([0,140])
        plt.xlim([0,len(datelen)])
        plt.axhline(y=0,color="black",linewidth=0.5)
        fig.suptitle("Buoy: " + str(time_thickness.Buoy.iloc[1]),fontsize=25,x=0.2)



        ax2 = ax1.twinx() 
        ax2.plot(time_thickness.Date, time_thickness["Air_Temp_(C)"],color="red",linewidth=1,ls="dashed")
        #ax2.set(xticks=[0,20, 40, 60, 80, 100, 120, 140])
        ax2.set(xticks=range(0, len(datelen), 10))
        ax2.set_ylabel("Air Temperature (Degrees C)",fontsize=15)

        legend_elements = [Line2D([0], [0], color='grey', lw=3, label='Snow Line'),
                           Patch(facecolor='azure',edgecolor='black',label='Ice'),
                           Patch(facecolor='navy', edgecolor='black',label='Ocean'),
                           Line2D([0], [0], color='red', lw=3, linestyle="--", label='Air Temp')]

        ax1.legend(handles=legend_elements, loc='center',bbox_to_anchor=(1.175, 0.5),labelspacing=2)
        
        
        
        plt.savefig(path +"\\" + str(buoy_id) + "_plot", bbox_inches='tight')
        time_thickness.to_csv(path +"\\" + str(buoy_id) + "dT120_thickness_data.csv",index=False)
        
        plt.show()
        
        
        
############################################

#class variables design
### 1) Buoy id
### 2) url for TEMP
### 3) url for HEAT
### 4) url for location
### 5) custom start date for this buoy

############################################



T56=Buoy("T56",
         "https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TEMP_proc.csv",
          "https://data.meereisportal.de/download/buoys/2019T56_300234065176750_HEAT120_proc.csv",
          "https://data.meereisportal.de/download/buoys/2019T56_300234065176750_TS.csv",
         "2019-12-01"
        )

T58=Buoy("T58",
         "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_TEMP_proc.csv",
        "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_HEAT120_proc.csv",
        "https://data.meereisportal.de/download/buoys/2019T58_300234065171790_TS.csv",
         "2019-12-01"
        )

T62=Buoy("T62",
         "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T62_300234068706290_TS.csv",
         "2019-12-01"
        )

T63=Buoy("T63",
         "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T63_300234068709320_TS.csv",
         "2019-12-01"
        )

T64=Buoy("T64",
        "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_TEMP_proc.csv",
        "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_HEAT120_proc.csv",
        "https://data.meereisportal.de/download/buoys/2019T64_300234068701300_TS.csv",
        "2019-12-01"
        )

T65=Buoy("T65",
         "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T65_300234068705730_TS.csv",
         "2019-12-01" 
        )

T66=Buoy("T66",
         "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T66_300234068706330_TS.csv", 
         "2019-12-01" 
        )

T68=Buoy("T68",
         "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T68_300234068708330_TS.csv",
         "2019-12-01" 
        )

T70=Buoy("T70",
         "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T70_300234068705280_TS.csv", 
         "2019-12-01" 
        )

T72=Buoy("T72",
         "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_TEMP_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_HEAT120_proc.csv",
         "https://data.meereisportal.de/download/buoys/2019T72_300234068700290_TS.csv",
         "2019-12-01" 
        )

#### to run for specific buoy, replace buoyid (in this case it is "T56" and run
# you can add any buoys you wish to by following the format above

T56.processbuoy()
