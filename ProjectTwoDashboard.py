# Setup the normal version of Dash
from dash import Dash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output


# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from AAC_ReadWrite import AnimalShelter



###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name. NOTE: You will
# likely need more variables for your constructor to handle the hostname and port of the MongoDB
# server, and the database and collection names

shelter = AnimalShelter()

MAX_UNIQUE_PIE_SLICES = 6

EMPTY_DATA = [{"Error":"one"},{"Error":"two"}]
EMPTY_COLUMNS = [{"name":"Error","id":"who knows"}]


# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(shelter.filter_none())

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)

#########################
# Dashboard Layout / View
#########################
app = Dash('SimpleExample')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.H3("by Marcus Doucette"),
    html.Hr(),
    dcc.RadioItems(
        ["Water Rescue","Mountain or Wilderness Rescue","Disaster or Individual Tracking","None"],
        "None",id="radio-buttons-id"),
    dash_table.DataTable(
        id='datatable-id',
        row_selectable='single',
        selected_rows=[0],
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        #FIXME: Set up the features for your interactive data table to make it user-friendly for your client

    ),
    html.Br(),
     html.Hr(),
     dcc.Graph(id="graph"),
     html.Div(
            id='map-id',
            className='col s12 m6',
            )
])

#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    out = [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns] if selected_columns else []
    return out


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
#FIXME Add in the code for your geolocation chart
    pass
    #viewData += shelter.read(index)
    dff = pd.DataFrame.from_dict(viewData)
    
    #retrieve exactly one row index
    if not index or (dff.to_dict('records')==EMPTY_DATA):
        row=-1
        dic = None
    else:
        row = index[0]
        dic = shelter.read_one({'':row})
    
    loc = [30,-97] if not dic else [dic["location_lat"],dic["location_long"]]
    
    return[
        dl.Map(style={'width':'1000px','height':'500px'},
              center=loc, zoom=10,children=[
                  dl.TileLayer(id='base-layer-id'),
                  dl.Marker(position=loc,
                    children=[
                        dl.Tooltip(dff.iloc[row,4]),
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(dff.iloc[row,9])
                        ]) if dff.iloc else []
                    ])
              ]) if row!=-1 else html.H1("???")
    ]

@app.callback(
    [Output("datatable-id","data"),
     Output("datatable-id","columns"),
     Output("graph","figure")
    ],
     Input("radio-buttons-id","value"))
def on_switch(value):
    if value=="Water Rescue":
        new_df = pd.DataFrame.from_records(shelter.filter_water_rescue())
    elif value == "Mountain or Wilderness Rescue":
        new_df = pd.DataFrame.from_records(shelter.filter_mountain_or_wilderness_rescue())
    elif value == "Disaster or Individual Tracking":
        new_df = pd.DataFrame.from_records(shelter.filter_disaster_or_individual_tracking())
    elif value == "None":
        new_df = pd.DataFrame.from_records(shelter.filter_none())
    if new_df.empty:
        print("Error")
        data = EMPTY_DATA
        columns = EMPTY_COLUMNS
        fig = None
    else:
        new_df.drop(columns=['_id'],inplace=True)
        data = new_df.to_dict('records')
        columns = [
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ]
        counts = new_df["breed"].value_counts()
        values = counts.head(MAX_UNIQUE_PIE_SLICES)
        others = counts[~counts.index.isin(values.index)]
        graph_set = pd.concat([values,pd.Series([others.sum()],index=["Other"])])
        #print(graph_set)
        fig = px.pie(graph_set,names=graph_set.index,values=graph_set.values)
        fig.update_layout(width=800,height=500)
    return data,columns, fig
            
app.run(debug=True)