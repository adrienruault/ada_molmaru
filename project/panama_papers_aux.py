import pandas as pd






class Item:
    """
    type_ should be either intermediaries, officers, entities or addresses
    """
    def __init__(self, node_id, name, country, type_):
        self.node_id = node_id
        self.name = name
        self.country = country
        self.type = type_
        
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
        entities = df_dictionary['entities']
        intermediaries = df_dictionary['intermediaries']
        officers = df_dictionary['officers']
        addresses = df_dictionary['addresses']
    
        type_ = 'entities'
        node_df = entities[entities['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'intermediaries'
            node_df = intermediaries[intermediaries['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'officers'
            node_df = officers[officers['node_id'] == node_id]
        if (node_df.empty):
            type_ = 'addresses'
            node_df = addresses[addresses['node_id'] == node_id]
        if (node_df.empty):
            item = cls.emptyInstance()
        else:
            name = node_df['name'].values[0]
            country = node_df['countries'].values[0]
            item = cls(node_id, name, country, type_)
            
        return item

    
    @classmethod
    def emptyInstance(cls):
        return cls(-1, -1, -1, -1)
            
            
            
            
            

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
            out_type = out_item.country
            
            new_df_line = pd.Series([in_node_id, in_name, in_country, in_type, relationship_elem.relationship, out_node_id,\
                                     out_name, out_country, out_type], index = output_columns)
            network_df = network_df.append(new_df_line, ignore_index = True)
            
        return network_df
        
        
        
        
        
        
        