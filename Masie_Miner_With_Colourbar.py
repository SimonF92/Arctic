import pandas as pd
import io
import requests
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,12))

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#add_change function calculates 10-day changes and bins them into strings
def add_change():
    
    #reading it back in just to avoid shuttling variables
    url="http://masie_web.apps.nsidc.org/pub/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv"
    df=pd.read_csv(url,header=1)
    df= df.tail(10)
    df= df.reset_index()
    dft = df.T
    #dft["Change"]=dft["9"]-dft["0"]
    dft
    #reset index as days from current
    dft = dft.set_axis(['0','1', '2', '3', '4', '5', '6', '7', '8', '9'], axis=1, inplace=False)
    #change is equal to current day minus day-10 previous
    dft["Change"]=dft["9"]-dft["0"]
    dft
    dft=dft.tail(17)
    dft

    dfchange=dft["Change"]
    dfchange
    
    #add change to full dataframe
    df2["Change"]=dft["Change"]

    #calculate percentage changes and rates of change
    df2["Rate"]=df2["Change"]/df2["Mean"]
    df2["Percentage_Change"]=df2["Change"]/df2["Mean"]*100
    df2["Ratesq"]=df2["Rate"]**2
    df2['10-day Trend'] = df2['Percentage_Change'].rank(pct=True)
    
    #bin rates of change into strings
    df2['ROC'] = "Strong Growth"
    df2['ROC'][df2["Rate"] > 0.05] = 'Strong Growth'
    df2['ROC'][(df2['Rate'] > 0) & (df2['Rate'] < 0.05)] = 'Growth'
    df2['ROC'][df2['Rate'] == 0] = "Stable"
    df2['ROC'][(df2['Rate'] < 0) & (df2['Rate'] > -0.05)]= "Decline"
    df2['ROC'][df2['Rate'] < -0.05] = "Strong Decline"
    
    #get nice header for ROC
    df2["10-day Rate of Change"] = df2["ROC"]
   
    
    return df2

#pull file from MASIE
url="http://masie_web.apps.nsidc.org/pub/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv"
df=pd.read_csv(url,header=1)


#select only decadal data
df["year"] = df['yyyyddd'].astype(str) 
df["year"]= df['year'].str[:4]
df["year"]=df["year"].astype(int)
df=df[df['year'].isin(range(2010,2022,1))]

#parse data to get day-of-year
df["day"] = df['yyyyddd'].astype(str) 
df["day"]= df['day'].str[4:]
df["day"]=df["day"].astype(int)


#pull most recent day from data
dftoday=df.tail(1)
today=dftoday["day"]


#call all data on todays date
dftodays=df[df['day'].isin(today)]

#take mean of decadal "todays"
dftodays.loc['Mean'] = dftodays.mean()
dftodaysmean=dftodays.tail(1)
dftodaysmean

#make dataframe of only today and today decadal means
frames = [dftoday, dftodaysmean]
dfplot= pd.concat(frames)

#make dataframe nice
dfplot.index = ["Current","Mean"]

#transpose dataframe prior to plot
dfplot_transposed = dfplot.T 
df2= dfplot_transposed

#calculate delta as "today" - "todays means"
df2["Delta"]=df2["Current"]-df2["Mean"]
df2["Delta2"]=df2["Delta"]/1000

#remove some extra stuff
df2=df2.tail(19)
df2=df2.head(17)
df2

#make region strings look nicer
df2['Region'] = df2.index
df2["Region"] = df2['Region'].astype(str) 
df2["Region"]= df2['Region'].str[5:]

#not used
df2["bins"]= pd.qcut(df2['Delta'], q=20)
#rank regions for colouring
df2['pct_rank'] = df2['Delta'].rank(pct=True)

#invoke add change from above
add_change()

#legend was being a pain so forced it to rank
custom_dict = {'Strong Growth':0, 'Growth':1, 'Stable':2, 'Decline':3, "Strong Decline": 4}  
df2['rank'] = df2['10-day Rate of Change'].map(custom_dict)
df2=df2.sort_values(by=['rank'])

#get today for the title in nice format
date=dftoday['yyyyddd'].to_string()
date=date.split(" ")
date= date[-1:]
date=str(date)
date=date.strip("']")
date=date.strip("['")

#was trying to create a colourbar legend but didnt like it

'''
plot = plt.scatter(data=df2,x="Delta2", y="Region",c="Percentage_Change", cmap='plasma')
plt.clf()
plt.colorbar(plot)
'''

#plot figure
#plt.style.use('classic')
#sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
sns.set(font_scale=1.3)
with sns.axes_style("whitegrid",{"xtick.major.size": 25}):
    ax = sns.barplot(x="Delta2", y="Region", hue= "10-day Rate of Change",palette="RdBu_r",data=df2,dodge=False,edgecolor=".2")
    ax.set(xlabel='Difference from 2010-2020 mean (1000km^2)', ylabel='Region',title='Date (year/ day): ' + date)


