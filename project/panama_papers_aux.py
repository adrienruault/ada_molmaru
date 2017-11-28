import pandas as pd
import folium
import math
import random




class Item:
    """
    type_ should be either Intermediary, Officer, Entity or Address
    """
    
    #static attribute containing the coordinates of the different capitals
    country_coordinates_path = './res/capital_coordinates.csv'
    
    capital_coordinates_df = -1
    
    def __init__(self, node_id, name, country, type_):
        self.node_id = node_id
        self.name = name
        self.country = country
        self.type = type_
        if (self.country == -1):
            self.latitude = -1
            self.longitude = -1
        else:
            self._getCountryCoordinates(country)
        print(self.country, 'latitude: {lat} / longitude: {lon}'.format(lat = self.latitude, lon = self.longitude))
        
    @classmethod
    def fromSingleLineDF(cls, single_line_df, type_):
        node_id = single_line_df['node_id'].values[0]
        name = single_line_df['name'].values[0]
        country = single_line_df['countries'].values[0]
        return cls(node_id, name, country, type_)
    
    # Method that creates an instance from a nodeId and from a dictionary of DataFrames
    # If the node is not in any of the DataFrames it outputs an empty node
    @classmethod
    def fromNodeId(cls, node_id, df_dictionary):
        entities = df_dictionary['Entity']
        intermediaries = df_dictionary['Intermediary']
        officers = df_dictionary['Officer']
        addresses = df_dictionary['Address']
    
        type_ = 'Entity'
        node_df = entities[entities['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'Intermediary'
            node_df = intermediaries[intermediaries['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'Officer'
            node_df = officers[officers['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'Address'
            node_df = addresses[addresses['node_id'] == node_id]
        if (node_df.empty):
            item = cls.emptyInstance()
        else:
            if (type_ == 'Address'):
                name = node_df['address'].values[0]
            else:
                name = node_df['name'].values[0]
            country = node_df['countries'].values[0]
            item = cls(node_id, name, country, type_)
            
        return item

    
    @classmethod
    def emptyInstance(cls):
        return cls(-1, -1, -1, -1)
    
    
    @classmethod
    def readCapitalCoordinates(cls):
        if (isinstance(cls.capital_coordinates_df, int)):
            cls.capital_coordinates_df = pd.read_csv(cls.country_coordinates_path)    
    
    
    # define latitude and longitude of the country. 
    # It is called in the Item constructor as soon as the country name is known
    def _getCountryCoordinates(self, country):
        #country_df = pd.read_csv('./res/country-capitals.csv')
        if (isinstance(self.capital_coordinates_df, int)):
            raise FileNotReadException('Please read the capital_coordinates.csv file before instantiating an Item object')
        
        # Some countries in the dataset are defined as several countries separated with a ';'
        # To get coordinates anyway we parse the country name in order to get the first country specified
        if (';' in country):
            country_array = country.split(';')
            country = country_array[0]
        
        if (country not in self.capital_coordinates_df['CountryName'].values):
            print(self.capital_coordinates_df.shape, country, 'not found in capital_coordinates.csv file')
            self.latitude = -1
            self.longitude = -1
        else:
            filtered_country_df = self.capital_coordinates_df[self.capital_coordinates_df['CountryName'] == country]
            self.latitude = filtered_country_df['CapitalLatitude'].values[0]
            self.longitude = filtered_country_df['CapitalLongitude'].values[0]

    
    def getDescription(self):
        return self.name + ' / ' + self.type + ' / ' + self.country
        
    
        
        
        
            

class SingleRelationship:
    """
    Class that represents the relationship between two items
    """
    
    def __init__(self, in_item, out_item, relationship):
        self.in_item = in_item
        self.out_item = out_item
        self.relationship = relationship
        
        
        
        
        
        
        
        
class ItemNetwork:
    """
    Class that represents all the relationships of a central item
    """
    
    def __init__(self, central_item, df_dictionary):
        
        # Attributes
        self.central_item = central_item
        self.relationship_list = []
        
        all_edges = df_dictionary['all_edges']
        
        in_relationship_df = all_edges[all_edges['node_2'] == central_item.node_id]
        out_relationship_df = all_edges[all_edges['node_1'] == central_item.node_id]

        in_node_id_list = in_relationship_df['node_1'].values
        out_node_id_list = out_relationship_df['node_2'].values

        # Looking for in-nodes throughout dataset
        for index, in_node_id in enumerate(in_node_id_list):
            in_item = Item.fromNodeId(in_node_id, df_dictionary)
            relationship = in_relationship_df['rel_type'].iloc[index]
            new_relationship = SingleRelationship(in_item, central_item, relationship)
            self.relationship_list += [new_relationship]

        # Looking for out-nodes throughout dataset
        for index, out_node_id in enumerate(out_node_id_list):
            out_item = Item.fromNodeId(out_node_id, df_dictionary)
            relationship = out_relationship_df['rel_type'].iloc[index]
            new_relationship = SingleRelationship(central_item, out_item, relationship)
            self.relationship_list += [new_relationship]

            
    def getDF(self):
        output_columns = ['in_node', 'in_name', 'in_country', 'in_type', 'relationship',\
                         'out_node', 'out_name', 'out_country', 'out_type']
        network_df = pd.DataFrame(columns = output_columns) 
        
        for relationship_elem in self.relationship_list:
            in_item = relationship_elem.in_item
            in_node_id = in_item.node_id
            in_name = in_item.name
            in_country = in_item.country
            in_type = in_item.type
            
            out_item = relationship_elem.out_item
            out_node_id = out_item.node_id
            out_name = out_item.name
            out_country = out_item.country
            out_type = out_item.type
            
            new_df_line = pd.Series([in_node_id, in_name, in_country, in_type, relationship_elem.relationship, out_node_id,\
                                     out_name, out_country, out_type], index = output_columns)
            network_df = network_df.append(new_df_line, ignore_index = True)
            
        return network_df
        
        
        
    def getMap(self):
        folium_map = folium.Map(location=[0, 0], zoom_start =2, min_zoom=2)
        feature_group = folium.map.FeatureGroup()
        
        color_dic = {'central_contour': '#ff0000', 'periph_contour': '#3388ff',\
                     'Entity': '#02f71a', 'Officer': '#01eef7', 'Intermediary': '#e6f701', 'Address': '#ffffff'}

        printed_node_id_list = [self.central_item.node_id]
        printed_coordinates = [self.central_item.latitude, self.central_item.longitude]
        
        for relationship_elem in self.relationship_list:
            item_pair = [(relationship_elem.in_item, relationship_elem.out_item)]
            
            for item in item_pair:
                if (item.node_id not in printed_node_id_list) and (item.country != -1) and (item.type != 'Address'):
                    current_latitude = item.latitude
                    current_longitude = item.longitude
                    if (current_latitude, current_longitude) in printed_coordinates:
                        print('Wooooooola')
                        radius = 2
                        coordinates[0] = coordinates[0] + radius * math.sin(2 * math.pi * random.random())
                        coordinates[1] = coordinates[1] + radius * math.cos(2 * math.pi * random.random())
                    else:
                        printed_coordinates += [coordinates]
                        
                    feature_group.add_child(
                        folium.features.CircleMarker(
                            [coordinates[0], coordinates[1]],
                            radius=8,
                            color=color_dic['periph_contour'],
                            fill_color=color_dic[item.type],
                            fill = True,
                            popup = item.getDescription(),
                            fill_opacity=0.6)
                        )
                    printed_node_id_list += [item.node_id]

        # central_item marker
        feature_group.add_child(
                    folium.features.CircleMarker(
                        [self.central_item.latitude, self.central_item.longitude],
                        radius=8,
                        color=color_dic['central_contour'],
                        fill_color=color_dic[self.central_item.type],
                        fill = True,
                        popup = self.central_item.getDescription(),
                        fill_opacity=0.6)
                    )   
                    
                  
        folium_map.add_child(feature_group)
        
        return folium_map
        
        


class FileNotReadException(Exception):
    pass
        
        