# Panama Papers : Where does the money come from ?

# Abstract

The Panama papers released in 2015 is the biggest leak of financial information in history. It came from the Panamanian corporate service company Mossack Fonseca. The leak revealed a substantial amount of illegal activities including fraud and tax evasion. It especially uncovered illegal financial activities carried out by world's biggest wealth holders, politicians and companies.

This project aims to compile the information provided by the Panama papers to show the geographical structure of offshore activities. We intend to do so thanks to an interactive map showing connections between the different entities and officers concerned by the leak. The idea being to make the information shown on the map scalable. As a concrete example, the user could query the structure of the offshore activities concerning a particular officer or intermediary but he/she could also scale up by querying offshore connections about more general entities like countries, tax heavens, continents, etc..


# Research questions

- Which countries were the most involved in the offshore activities unveiled in the leak?
- What are the relationships between countries and tax heavens? 
- Are there evidences of privileged relationships between some countries and tax heavens?
- Is there an evolution in time of the tax heavens activity?


# Dataset

The dataset is taken from https://www.occrp.org/en/panamapapers/database and it contains five csv files that are described below: 
- Entities.csv, Officers.csv, Intermediaries.csv are dedicated to the three types of actors encountered in the database. Entities refer to asset providers and officers to financial actors (company, private client, ...). Intermediaries refer to actors putting clients and financial service providers in contact.
- Addresses.csv describe all the addresses contained in the database those addresses are linked to officers.
- all_edges.csv describe the relationships between the items of the database described before, that are entities, officers, intermediaries and addresses. Four different kinds of relationships are described in this dataset: 'registered address', 'shareholder of', 'beneficiary of' and 'intermediary of'.

Note that the dataset is also provided under the neo4j format.



# A list of internal milestones up until project milestone 2

1. **Simple queries**: implementation of simple requests on the dataset's items. e.g. return an actor or a group of actors by querying a name or part of a name. The query will be completed by applying filters on the actor type (entity, officer or intermediary) and on the actor's country.
2. **Map pointers**: Connect the simple queries of items to a GUI interface showing the world map. By querying an item, its country would get pointed on the map. The pointer will be colored according to the item type.
3. **Macroscopic queries**: implementation of queries about macroscopic information of the dataset. The queries should ouput information about the level of offshore activities in a country or region
4. **Density map**: create an interactive density map, which can show the level of offshore activities in countries or regions.
5. **Connection queries**: implementation of queries that show the relationships between the queried actor and the other actors of the database (entity, officer, intermediary). The query should specify the nature of the relationships (shareholder of, beneficiary of, intermediary of).
6. **Connection map**: Integrate the relationship queries in the interactive map the queried actor's relationship are geographically visualizable. A color code should allow good understanding of relationship types.
7. **Macroscopic connections**: implementation of queries able to show the breadth of the connections between countries and tax heavens. 
8. **Map finalization**: integration of the macroscopic connections in the interactive map.
 
![Alt text](./res/gantt_chart.png?raw=true "Gantt chart")

Add here a sketch of your planning for the next project milestone.

# Questions for TAa

Should we make a time line analysis or just concentrate on present (2015) ?

Add here some questions you have for us, in general or project-specific.
