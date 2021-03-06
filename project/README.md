# Panama Papers : Where does the money come from ?

## Website of the project

A website describing the features of the project is available [here](https://hadrienmarcellin.github.io/ada_jekyll_page/) along with its [github repository](https://github.com/HadrienMarcellin/ada_jekyll_page).

## Abstract

The Panama papers released in 2015 is the biggest leak of financial information in history. It came from the Panamanian corporate service company Mossack Fonseca. The leak revealed a substantial amount of illegal activities including fraud and tax evasion. It especially uncovered illegal financial activities carried out by world's biggest wealth holders, politicians and companies.

This project aims to compile the information provided by the Panama papers to show the geographical structure of offshore activities. We intend to do so thanks to an interactive map showing connections between the different entities and officers concerned by the leak. The idea being to make the information shown on the map scalable. As a concrete example, the user could query the structure of the offshore activities concerning a particular officer or intermediary but he/she could also scale up by querying offshore connections about more general entities like countries, tax heavens, continents, etc..


## Research questions

- Which countries were the most involved in the offshore activities unveiled in the leak?
- What are the relationships between countries and tax heavens? 
- Are there evidences of privileged relationships between some countries and tax heavens?
- Is there an evolution in time of the tax heavens activity?



## A list of internal milestones

1. **Simple queries**: implementation of simple requests on the dataset's items. e.g. return an actor or a group of actors by querying a name or part of a name. The query will be completed by applying filters on the actor type (entity, officer or intermediary) and on the actor's country.
2. **Map pointers**: Connect the simple queries of items to a GUI interface showing the world map. By querying an item, its country would get pointed on the map. The pointer will be colored according to the item type.
3. **Macroscopic queries**: implementation of queries about macroscopic information of the dataset. The queries should ouput information about the level of offshore activities in a country or region
4. **Density map**: create an interactive density map, which can show the level of offshore activities in countries or regions.
5. **Connection queries**: implementation of queries that show the relationships between the queried actor and the other actors of the database (entity, officer, intermediary). The query should specify the nature of the relationships (shareholder of, beneficiary of, intermediary of).
6. **Connection map**: Integrate the relationship queries in the interactive map the queried actor's relationship are geographically visualizable. A color code should allow good understanding of relationship types.
7. **Macroscopic connections**: implementation of queries able to show the breadth of the connections between countries and tax heavens. 
8. **Map finalization**: integration of the macroscopic connections in the interactive map.
 
 
![Alt text](./res/gantt_chart.png?raw=true "Gantt chart")





## Data description

### Note following the Paradise papers leak

##### Changes in the dataset formatting

The format of the datasets have been changed since Milestone 1. Indeed following the release of the Paradise Papers leak the International Consortium of Investigative Journalists (ICIJ) have slightly modified the way of presenting their data. Indeed before the Paradise papers leak the data concerning previous leaks was gathered as a single dataset. This dataset used to include the Panama papers, the Offshore leaks and the Bahamas leaks. Recently then the ICIJ has decided to present their data in a slightly different way. The framework in which it is stored is roughly the same which allows our implementations to keep working. However their strategy is to display the data by leak rather than as a single whole block. This involves slight changes in the preprocessing of the data but nothing dramatic.


##### New perspectives brought by the Paradise papers leak

Despite this little update of the dataset presentation the release of the Paradise papers offers new perspectives to the present project. Indeed it makes available new fresh data to analyze and thus complete the former dataset. It also brings more interest to our study given that the case is still a hot topic in the news. Then the fact that the Paradise papers dataset is formated in the same manner as the previous ones makes it very easy to embed in our implementation.

Finally it is important to precise that the Paradise papers dataset available in the ICIJ website does not contain the entire leak. Indeed only documents from the Appleby law office are available. The whole leak is expected to be publicly released in a matter of weeks. For this reason the treatment of this particular dataset with our implementation is not fully guaranteed yet, given its instability.


### Download the dataset

The datasets for the four leaks is available at https://offshoreleaks.icij.org/pages/database. In order to run our implementation properly please download the datasets from the website as a zip file. Then unzip it in `./data/data_csv/`. Running the `main_pipeline.ipynb` or the `preprocessing.ipynb` notebook will read the data, clean and save them in a way to be readable by our implementation. 


### Framework of the dataset

The four datasets corresponding to each of the leaks described previously are organized in the same way and they all contain the same files. Those files are described below:

- **Entities.csv**, **Officers.csv**, **Intermediaries.csv** are dedicated to the three types of actors encountered in the database. Entities refer to asset providers and officers to financial actors (company, private client, ...). Intermediaries refer to actors putting clients and financial service providers in contact.
- **Addresses.csv** describe all the addresses contained in the database those addresses are linked to officers.
- **all_edges.csv** describe the relationships between the items of the database described before, that are entities, officers, intermediaries and addresses. Four different kinds of relationships are described in this dataset: 'registered address', 'shareholder of', 'beneficiary of' and 'intermediary of'.

The dataset is also provided under the neo4j format. However this is not planned to be used in the frame of this project.






## Running the jupyter notebook implementation


#### Prerequisites

The implementation is quaranteed to run with the following specifications:
- `jupyter notebook` version: 4.3.0
- `ipywidgets` version: 7.0.0
- `folium` version: 0.5.0
- `geopandas` version: 0.3.0


#### Where to locate the datasets

Download the `Bahamas Leaks`, `Offshore Leaks`, `Panama papers` and `Paradise papers` zip files through [official website](https://offshoreleaks.icij.org/pages/database) or through this [google drive shareable link](https://drive.google.com/drive/folders/1Jt7ip-O0Ms11rbndgNBJq4tnC7y-JUCB?usp=sharing). Then unzip them and place the csv files in their corresponding folder following the structure specified below. All the files and folders marked by `(*)` are generated by `preprocessing.ipynb` or `main_pipeline.ipynb`.

```
./project/
+-- data
|   +-- data_csv
|       +-- Entities.csv (*)
|       +-- Intermediaries.csv (*)
|       +-- Officers.csv (*)
|       +-- Addresses.csv (*)
|       +-- all_edges.csv (*)
|       +-- bahamas_leaks
|           +-- bahamas_leaks.edges.csv
|           +-- bahamas_leaks.nodes.address.csv
|           +-- bahamas_leaks.nodes.entitiy.csv
|           +-- bahamas_leaks.nodes.intermediary.csv
|           +-- bahamas_leaks.nodes.officer.csv
|       +-- offshore_leaks
|           +-- offshore_leaks.edges.csv
|           +-- offshore_leaks.nodes.address.csv
|           +-- offshore_leaks.nodes.entitiy.csv
|           +-- offshore_leaks.nodes.intermediary.csv
|           +-- offshore_leaks.nodes.officer.csv
|       +-- panama_papers
|           +-- panama_papers.edges.csv
|           +-- panama_papers.nodes.address.csv
|           +-- panama_papers.nodes.entitiy.csv
|           +-- panama_papers.nodes.intermediary.csv
|           +-- panama_papers.nodes.officer.csv
|       +-- paradise_papers
|           +-- paradise_papers.edges.csv
|           +-- paradise_papers.nodes.address.csv
|           +-- paradise_papers.nodes.entitiy.csv
|           +-- paradise_papers.nodes.intermediary.csv
|           +-- paradise_papers.nodes.officer.csv
|    +-- data_clean_csv (*)
```

The `preprocessing.ipynb` and `main_pipeline.ipynb` should run well if the data files are organized this way.

#### Project files

- `main_pipeline.ipynb`: includes the whole pipeline of the project including the preprocessing, the density maps and the connection queries.
- `preprocessing.ipynb`: implements the preprocessing of the datasets. It cleans them and saves them in the `./data/data_clean_csv/` folder.
- `connection_queries.ipynb`: implements of the connection queries alone. It requires `preprocessing.ipynb` to be run before using it.
- `density_map.ipynb`: implements the density map alone. It requires `preprocessing.ipynb` to be run before using it.
- `panama_papers_aux.py` and `desnity_maps.py`: contains helpers for the `.ipynb` notebooks.




## Future of the project

Following the milestones described previously the project has taken two different paths. 

- The first direction is the implementation of a density map generator to illustrate the level of offshore activities in the world. One of the reason for these density maps is that they give the ability to compare countries and to quickly identify the behavior of some countries regarding offshore activities. This task is interesting because it offers many ways of presenting the data. Indeed quantifying the level of offshore activities is not a well defined concept and it is thus subject to interpretation.


- The second direction is the development of a connection query tool. This tool allows to retrieve all the items of the database that a company or an individual is connected to. It then creates a network that is displayed on a folium map and whose vertices are the queried item along with its connections. The tool is intended to graphically show 


##### Future orientation

The most important remaining tasks of the project are described in the milestones section of the present README.md.
Moreover until now both the **density map** and **connection query** implementations have followed disjoint paths but it is planned to unite both implementations in the end in order to create a GUI that is easy to use for non-jupyter notebook users. Ideally this GUI would contain a unique map on which most of the queries could be made. 

The creation of a jupyter-dashboard is also planned in order to be able to share the application to everyone, even non-programmers. Indeed we believe that it is with no coding interface that the application could have the greatest impact. 


## Run locally the future Web App

An implementation of the web app is available in the repository, but for the moment it is not hosted on any public website.
It is however possible to run it locally installing the python package Bokeh (pip install bokeh) and executing the following command in the actual folder:

bokeh serve --show main.py



