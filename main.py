import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import io
import base64
import requests
import json

"""Fetchind Data from sources"""


def fetch_data():
    response = requests.get("https://api.covid19india.org/data.json")
    data = dict(json.loads(response.text))
    response_data = pd.DataFrame(data['statewise'])
    state_data = response_data[['state', 'active', 'confirmed', 'deaths', 'recovered']]
    state_data['state'] = state_data['state'].map(lambda x: x.lower())

    for col in ['active', 'confirmed', 'deaths', 'recovered']:
        state_data[col] = state_data[col].astype(int)

    state_data['death%'] = (state_data['deaths'] / state_data['confirmed']) * 100
    state_data['cure%'] = (state_data['recovered'] / state_data['confirmed']) * 100

    state_data.replace('telangana', 'andhra pradesh', inplace=True)
    state_data.replace('jharkhand', 'bihar', inplace=True)
    state_data.replace('chhattisgarh', 'madhya pradesh', inplace=True)
    state_data.replace('uttarakhand', 'uttar pradesh', inplace=True)
    state_data.replace('odisha', 'orissa', inplace=True)
    state_data.replace('puducherry', 'pondicherry', inplace=True)
    state_data.replace('ladakh', 'jammu and kashmir', inplace=True)

    return state_data


"""Importing the Graph Data"""


def fetch_map():
    graph_data = gpd.read_file('graph_data//india_ds.shp')
    graph_data['STATE'] = graph_data['STATE'].map(lambda x: x.lower())

    graph_data['STATE'].replace('dadra and nagar haveli', "dadra and nagar haveli and daman and diu", inplace=True)
    graph_data['STATE'].replace('daman and diu', "dadra and nagar haveli and daman and diu", inplace=True)

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
                # my_stringIObytes = cStringIO.StringIO()
                # every_map.savefig(my_stringIObytes, format='jpg')
                # my_stringIObytes.seek(0)
                # map_to_base64 = base64.b64encode(my_stringIObytes.read())

                pic_IObytes = io.BytesIO()
                plt.savefig(pic_IObytes, format='png')
                pic_IObytes.seek(0)
                map_to_base64 = base64.b64encode(pic_IObytes.read())

                yield map_to_base64

        base64_maps = generate_base64()

        return {"confirmed": str(type(next(base64_maps)))}
                # "death": next(base64_maps),
                # "cured": next(base64_maps),
                # "active": next(base64_maps),
                # "death_percent": next(base64_maps),
                # "cured_percent": next(base64_maps)}

    except Exception as e:
        return str(e)
