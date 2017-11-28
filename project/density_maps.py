import pandas as pd
import folium
import json
import geopandas
import branca.colormap as cm


# The main function to create the density map. It loads the geoJSON and the csv file queried.
# It makes then match the countries of the geoJSON file with the countries of the csv file and
# call the get_color_map function before adding the choroplet to the map.
# Finally, it prints the countries that are in the csv file but not in the geoJSON.
def create_density_map(query, json_weight, region):

    mymap = folium.Map()
    geo_df_world = geopandas.read_file('./data/geojson/world_' + json_weight + '.json')
    geo_df = geo_df_world
    if (region != 'World'):
        geo_df = geo_df[geo_df['region_un'] == region]
    
    data_clean = pd.read_csv('./data/data_clean_csv/' + query + '_clean.csv', dtype = 'object')

    data_name_id = data_clean[['name','country_codes']].dropna().drop_duplicates()
    data_name_id = data_name_id[(data_name_id['country_codes'].isin(geo_df['adm0_a3_is']))]
    count_df = pd.DataFrame([], geo_df['adm0_a3_is'].drop_duplicates())
    count_df['count'] = pd.np.zeros([len(count_df.index)])
    
    for key in count_df.index:
        count_df.loc[key,'count'] = len(data_name_id[data_name_id['country_codes'] == key])
        
    colormap = get_color_map_log(count_df)
    
    folium.GeoJson(
        geo_df,
        name='properties',
        style_function=lambda feature: {
            'fillColor': colormap(my_log10(count_df.loc[feature['properties']['adm0_a3_is'],'count'])),
            'color': 'black',
            'weight': 1,
            'dashArray': '5, 5',
            'fillOpacity': 0.9,
        }
    ).add_to(mymap)

    colormap.add_to(mymap)
    colormap.caption ='Number of ' + query + ' per country (log scale, base 10)'
    
    
    df_countries = data_clean[['countries','country_codes']].dropna().drop_duplicates()
    df_countries = df_countries[pd.np.logical_not(df_countries['country_codes'].str.contains(';'))]
    print('Countries not present in the geoJSON:')
    print(df_countries[pd.np.logical_not(df_countries['country_codes'].isin(geo_df_world['adm0_a3_is']))]['countries'])

    return mymap

# We define our own log function so that when we have 0 actor in a country, it is considered to be a 0 in log scale.
def my_log10(a):
    if(a == 0):
        return 0
    else:
        return pd.np.log10(a)

# We choose to use a logarithmic scale for the choroplet, because it is more readable and provides more contrast on the map.
def get_color_map_log(count_df):
    log_count = pd.np.log10(count_df[count_df['count'] != 0]['count'])
    
    vmax = log_count.max()
    
    colormap = cm.LinearColormap(
        colors=['white','yellow','red'],
        vmin=0,
        vmax=vmax
    )
    #index=count_df['count'].quantile([0,.2,.4,.6,.8,1.0]
    #colormap = colormap.to_step(n=4,index=[0,100,1000,5000,10000,26825])
    #colormap = colormap.to_step(n=100, data=log_count, method='quantiles')
    
    
    return colormap