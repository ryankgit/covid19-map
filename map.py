# COVID-19 data gathered from https://github.com/GoogleCloudPlatform/covid-19-open-data

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Get data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
location_data = pd.read_csv("https://storage.googleapis.com/covid19-open-data/v2/geography.csv",
                            usecols=['key',
                                     'latitude',
                                     'longitude'])
epidemiology_data = pd.read_csv("https://storage.googleapis.com/covid19-open-data/v2/epidemiology.csv",
                                usecols=['date',
                                         'key',
                                         # 'total_confirmed',
                                         # 'total_deceased',
                                         # 'total_recovered',
                                         'total_tested'])
# TODO: only read most recent data if possible (?)

# create geometry out of long and lat provided in location_data
location_data = gpd.GeoDataFrame(location_data,
                                 geometry=gpd.points_from_xy(
                                     location_data.longitude,
                                     location_data.latitude))
print(location_data.head(5))

# merge csv tables on key
epidemiology_location_data = location_data.merge(epidemiology_data, on='key')
print(epidemiology_location_data.head(5))

# plot separate world and epidemiology_location_data layers
plt.rcParams['figure.figsize'] = 8, 6
fig, ax = plt.subplots()
ax.set_aspect('equal')
print(world.head())

world.plot(ax=ax, color='white', edgecolor='black', zorder=1)
# TODO: specify which column of data to plot, only plot most recent date.
#   Change point to heatmap based on associated value
epidemiology_location_data.plot(column='total_tested', ax=ax, marker='o', markersize=0.1, zorder=2)

plt.show()