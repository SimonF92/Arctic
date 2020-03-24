#! pip install seaborn
#! pip install matplotlib


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,10))


g = sns.FacetGrid(full_dataset, col="Buoy",col_wrap=3)

######
#change anything in red below to anything you want
######

g.map(plt.plot, "date", "Ice_Water_Thermistor", alpha=.7)
g.map(plt.plot, "date", "Ice_Snow_Thermistor", alpha=.7,color="red")
g.map(plt.plot, "date", "Snow_Air_Thermistor", alpha=.7,color="green")
g.set(xticks=[35, 70, 105, 140])
for ax in g.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(45)