import geopandas as gpd
import pandas as pd
import numpy as np
import mapclassify
import matplotlib.pyplot as plt
import base64

# Plotter Making and preprocessing using Geopandas

shape_file = 'India_Districts_ADM2_GADM.shp'

plotter = gpd.read_file(shape_file)[['STATE', 'geometry']]


def title(state):
    return state.title()


plotter['STATE'] = plotter['STATE'].apply(title)

wrong = ['Andaman And Nicobar Islands', 'Dadra Nagar Haveli',
         'Daman And Diu',
         'Jammu And Kashmir',
         'Odissa',
         'Pondicherry']

right = ['Andaman and Nicobar Islands',
         'Dadra and Nagar Haveli',
         'Daman and Diu',
         'Jammu and Kashmir',
         'Odisha',
         'Puducherry']

for n in range(len(wrong)):
    plotter['STATE'].replace(wrong[n], right[n], inplace=True)


# Requesting the content from the Ministry of Health and Family Welfare
def pull_data():
    dfs = pd.read_html('https://www.mohfw.gov.in/')
    live_data = dfs[0]
    live_data = live_data.iloc[:35, :]
    for col in ['Active Cases*', 'Cured/Discharged/Migrated*', 'Deaths**', 'Total Confirmed cases*']:
        live_data[col] = live_data[col].astype(int)
    live_data['Death%'] = (live_data['Deaths**'] / live_data['Total Confirmed cases*']) * 100
    live_data['Cured%'] = (live_data['Cured/Discharged/Migrated*'] / live_data['Total Confirmed cases*']) * 100

    # Merging the two findings and plotting

    merge_data = plotter.merge(live_data, right_on='Name of State / UT', left_on='State_Name', how='inner')

    plot_data = gpd.GeoDataFrame(merge_data)
    return plot_data


# plotting the data and convert to Base64

def map_plotter(data, param):
    data.plot(column=param, figsize=(20, 10), legend=True, edgecolor='green', cmap='OrRd', scheme='quantiles')
    plt.savefig('map_image.jpg')
    with open("map_image.jpg", "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    return encoded_string


def generate():
    plot_data = pull_data()
    maps = {"confirmed": map_plotter(plot_data, "Total Confirmed cases*"),
            # "active": map_plotter(plot_data, "Active Cases*"),
            # "cures": map_plotter(plot_data, "Cured/Discharged/Migrated*"),
            # "death": map_plotter(plot_data, "Deaths**"),
            # "cure%": map_plotter(plot_data, "Cured%"),
            # "death%": map_plotter(plot_data, "Death%")}

    return maps
