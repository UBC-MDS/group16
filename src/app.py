from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Map'),
    html.P("Year:"),
    dcc.RadioItems(
        id='year', 
        options=["2017", "2018", "2019","2020","2021"],
        value="2021",
        inline=True
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("year", "value"))
def display_choropleth(year):
    df = pd.read_csv(r"../data/processed/map_df.csv")#px.data.election() # replace with your own data source
    df = df[df['year']==int(year)]
    geojson = gpd.read_file("../data/vancouver.geojson")#px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color= df['count'],
        locations="name", featureidkey="properties.name",
        projection="mercator", #range_color=[0, df.count],
        color_continuous_scale='YlOrRd')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


app.run_server(debug=True)