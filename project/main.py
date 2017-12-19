from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource
from bokeh.sampledata.sample_geojson import geojson
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool, Button,
  Dropdown, RadioButtonGroup, Select, Line, MultiLine, HoverTool, TapTool
)

from numpy.random import random

from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select, TextInput
import pandas as pd
import numpy as np
#import branca
import panama_papers_aux

GOOGLE_MAP_API_KEY = 'AIzaSyB5VErq0qJIh0dyztF4ZZbkivhFGpooKKQ'


entities = pd.read_csv("./data/data_clean_csv/entities_clean.csv", dtype = 'object')
intermediaries = pd.read_csv("./data/data_clean_csv/intermediaries_clean.csv", dtype = 'object')
officers = pd.read_csv("./data/data_clean_csv/officers_clean.csv", dtype = 'object')
addresses = pd.read_csv("./data/data_clean_csv/addresses_clean.csv", dtype = 'object')
all_edges = pd.read_csv("./data/data_clean_csv/all_edges_clean.csv", dtype = 'object')

df_dictionary = {'Entity': entities, 'Intermediary': intermediaries, 'Officer': officers, 'Address': addresses,
             'all_edges': all_edges}

available_countries = [x for x in officers['countries'].unique() if ';' not in x]
available_countries.sort()
available_countries = ['All'] + available_countries
len(available_countries)

#input = TextInput(value=str(len(available_countries)))



panama_papers_aux.Item.readCapitalCoordinates()

map_options = GMapOptions(map_type="roadmap", zoom=1)

plot = GMapPlot(plot_width=666, plot_height=400, x_range=Range1d(), y_range=Range1d(), map_options=map_options)

plot.api_key = GOOGLE_MAP_API_KEY

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

# source = ColumnDataSource(
#             data=dict(
#                 lat=[30.29, 30.20, 30.29],
#                 lon=[-97.70, -97.74, -97.78],
#             )
#         )
#
# circle = Circle(x="lon", y="lat", fill_color="blue", fill_alpha=0.8, line_color=None, name='Austin')

#
#
# def showAustin(*args):
#     plot.add_glyph(source, circle)

def reinitMap(*args):
    plot.renderers.pop()



# btnshow = Button(label="generate a point on Austin")
# btnshow.on_click(showAustin)

btnremove = Button(label="Reinitialize the map")
btnremove.on_click(reinitMap)




##### WIDGETS CREATION

options_type_dic = {'Entities': 'entities', 'Intermediaries': 'intermediaries', 'Officers': 'officers'}

option_list = ['Entity', 'Intermediary', 'Officer']

widgetDFName = radio_button_group = RadioButtonGroup(
        labels=option_list, active=0)

widgetQueriedName = TextInput(title = 'Name', value = 'Type name here')

widgetCountry = Select(title = 'Country', options = available_countries)

widgetResult = Select(title = 'Name options')

matched_df = None

def showResults(*args):
    global matched_df
    matched_df = panama_papers_aux.search_by_name(queried_name=widgetQueriedName.value,
                                                            dictionary=df_dictionary,
                                                            df_name=widgetDFName.labels[widgetDFName.active],
                                                            country=widgetCountry.value)
    widgetResult.options = matched_df['name'].values.tolist()

def showRelations(*args):
    name = widgetResult.value
    if((name == None)):
        return
    selected_name_df = matched_df[matched_df['name'] == widgetResult.value]

    # Instantiating an Item object corresponding to the query
    # Then instantiating a NetworkItem object from the previous Item object
    type_ = widgetDFName.labels[widgetDFName.active]
    queried_item = panama_papers_aux.Item.fromSingleLineDF(selected_name_df, type_)
    queried_item_network = panama_papers_aux.ItemNetwork(queried_item, df_dictionary)

    # get ItemNetwork DataFrame and print it
    network_df = queried_item_network.getDF()
    textResult.value = network_df.to_string()

    (dict_map, edge_dict) = queried_item_network.getBokehMap()

    source = ColumnDataSource(
        data=dict_map
    )

    edges_source = ColumnDataSource(data=edge_dict)

    circle = Circle(x="lon", y="lat", size=15,
                    fill_color="fill_color",
                    line_color="color", name='point',
                    fill_alpha=0.6, line_cap='round', line_width=2)

    plot.add_glyph(source, circle)

    lines = MultiLine(xs="lon", ys="lat", line_color="black", line_width=2)
    plot.add_glyph(edges_source, lines)

    plot.tools.pop()
    plot.add_tools(HoverTool(tooltips=[("item_description", "@item_description")]))

    #taptool = plot.select(type=TapTool, name='point')
    #taptool.callback = branch('@type', '@myname')



def branch(type, name):
    print(type)
    print(name)




button1 = Button(label="Apply Filter")
button1.on_click(showResults)

button2 = Button(label="Display Relationships")
button2.on_click(showRelations)

textResult = TextInput()


# create a layout for everything
mylayout = layout(
    children=[[btnremove], [widgetDFName, widgetQueriedName], [widgetCountry, widgetResult],
                [button1, button2], [plot]])
# add the layout to curdoc
curdoc().add_root(mylayout)
#COUNT = 0
#curdoc().add_periodic_callback(update(COUNT), 150)





