import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import cStringIO
import base64

"""Fetchind Data from sources"""


def fetch_data():
    response = pd.read_html("https://www.mohfw.gov.in/")
    in_data = response[0]
    in_data = in_data.iloc[:35, :]
    in_data.columns = ['Sno', 'state', 'active', 'cured', 'death', 'confirmed']
    for col in ['active', 'cured', 'death', 'confirmed']:
        in_data[col] = in_data[col].astype(int)
    in_data['death%'] = (in_data['death'] / in_data['confirmed']) * 100
    in_data['cure%'] = (in_data['cured'] / in_data['confirmed']) * 100
    in_data['state'] = in_data['state'].map(lambda x: x.lower())

    in_data.replace("chhattisgarh", "bihar", inplace=True)
    in_data.replace("jharkhand", 'bihar', inplace=True)
    in_data.replace("dadar nagar haveli", 'dadar and nagar haveli', inplace=True)
    in_data.replace("odisha", 'orissa', inplace=True)
    in_data.replace("ladakh", 'jammu and kashmir', inplace=True)
    in_data.replace("telengana", 'andhra pradesh', inplace=True)
    in_data.replace("uttarakhand", 'uttar pradesh', inplace=True)

    state_data = in_data.groupby(by='state').sum()

    return state_data


"""Importing the Graph Data"""


def fetch_map():
    graph_data = gpd.read_file('india_ds.shp')
    graph_data['STATE'] = graph_data['STATE'].map(lambda x: x.lower())

    graph_data.replace("pondicherry", 'puducherry', inplace=True)

    return graph_data


"""Creaeting Merged Dataframe"""


def generate_results():
    state_details = fetch_data()
    graph_details = fetch_map()

    my_map = graph_details.merge(state_details, right_on='state', left_on='STATE')
    try:
        def generate_heatmap():
            for column_name in ["confirmed", 'death', 'cured', 'active', 'death%', 'cured%']:
                yield my_map.plot(column=column_name, figsize=(20, 10), legend=True, edgecolor='black', cmap='OrRd',
                                  scheme='quantiles')

        maps = generate_heatmap()

        def generate_base64():

            for every_map in maps:
                my_stringIObytes = cStringIO.StringIO()
                every_map.savefig(my_stringIObytes, format='jpg')
                my_stringIObytes.seek(0)
                map_to_base64 = base64.b64encode(my_stringIObytes.read())
                yield map_to_base64

        base64_maps = generate_base64()

        return {"confirmed": next(base64_maps),
                "death": next(base64_maps),
                "cured": next(base64_maps),
                "active": next(base64_maps),
                "death_percent": next(base64_maps),
                "cured_percent": next(base64_maps)}

    except Exception as e:
        return str(e)
