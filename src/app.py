from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import utm
import geopandas as gpd
import dash_daq as daq

alt.data_transformers.disable_max_rows()


def load_gdf():
    # load geographical data for Vancouver
    # https://opendata.vancouver.ca/explore/dataset/local-area-boundary/export/?disjunctive.name&location=12,49.2474,-123.12402
    gdf = gpd.read_file("../data/van_spatial_data")
    return gdf


def load_nb():
    # load geo coordenates for each neighbourhood in Vancouver. Rename districts to match naming convention from VPD
    # https://opendata.vancouver.ca/explore/dataset/local-area-boundary/export/?disjunctive.name&location=12,49.2474,-123.12402
    nb = pd.read_csv(r"../data/van_neighbourhoods.csv", sep=";")
    nb["geo_point_2d"] = nb["geo_point_2d"].apply(
        lambda x: np.fromstring(x, dtype=np.double, sep=",")
    )
    nb[["nb_lat", "nb_lon"]] = pd.DataFrame(
        nb["geo_point_2d"].to_list(), columns=["nb_lat", "nb_lon"]
    )
    nb = nb.rename(columns={"Name": "Neighborhood"})
    nb.loc[nb.Neighborhood == "Arbutus-Ridge", "Neighborhood"] = "Arbutus Ridge"
    nb.loc[nb.Neighborhood == "Downtown", "Neighborhood"] = "Central Business District"
    return nb[["Neighborhood", "nb_lat", "nb_lon"]]


def prep_map_data(df, nbs=[], yrs=[]):
    # filters dataset by neighbourhood/ years and add geo coordenates
    # load coordenates of Van neighborhoods
    van_nb = load_nb()
    if nbs:
        df = df[df.Neighborhood.isin(nbs)]
    if yrs:
        df = df[df.YEAR.isin(yrs)]
    # group by Neighborhood (default = all neighborhoods)
    df_filtered = df.groupby("Neighborhood").size().reset_index(name="Crimes")
    # add centre geo coordenates for each neighbourhood
    df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")
    return df_filtered


def preprocessing_dataset(df):
    # eliminate data sets without coordenates
    df = df[df["HUNDRED_BLOCK"] != "OFFSET TO PROTECT PRIVACY"]
    df.reset_index(drop=True, inplace=True)
    # rename columns
    df = df.rename(columns={"NEIGHBOURHOOD": "Neighborhood", "TYPE": "Type"})
    # convert coordenates
    pp_df = df.copy()
    pp_df.loc[:, "lat"], pp_df.loc[:, "lon"] = utm.to_latlon(
        pp_df["X"], pp_df["Y"], 10, "n", strict=False
    )
    return pp_df


# load Van map
gdf = load_gdf()

# load crimes data
filename = "../data/processed/merged_df.csv"
df = pd.read_csv(filename, index_col=0)

# Preprocessing crimes data = eliminate missing coordinates and update col names/ neighborhoods
df = preprocessing_dataset(df)

# inspect distribution by year
df.groupby("YEAR").size().reset_index(name="Crimes")

agg_df = prep_map_data(df)

base = alt.Chart(gdf).mark_geoshape(stroke="gray", fill=None)

pts = (
    alt.Chart(agg_df)
    .mark_circle()
    .encode(
        latitude="nb_lat",
        longitude="nb_lon",
        size="Crimes",
        color=alt.Color("Crimes", scale=alt.Scale(scheme="yelloworangered")),
        tooltip=["Neighborhood", "Crimes"],
    )
)

final = base + pts


# read the data
data = pd.read_csv("../data/processed/merged_df.csv", index_col=0)
daytime = range(6, 19)
data["TIME"] = np.where(data.HOUR.isin(daytime), "day", "night")


app = Dash(
    __name__,
    title="Vancouver Crime Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

barchart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("TYPE"),
        y=alt.Y("count(TYPE)"),
        color=alt.Color("TYPE", scale=alt.Scale(scheme="yelloworangered"), legend=None),
    )
)

lineplot = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x=alt.X("YEAR:O", title="Year"),
        y=alt.Y("count(HOUR)", scale=alt.Scale(domain=[13000, 28000])),
        color=alt.Color(
            "TIME", scale=alt.Scale(scheme="yelloworangered"), title="Time"
        ),
    )
    .properties(width=1000, height=200)
)


server = app.server
plot_body = [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Iframe(
                        srcDoc=barchart.to_html(),
                        style={
                            "border-width": "0",
                            "width": "100%",
                            "height": "400px",
                        },
                    )
                ],
            ),
            dbc.Col(
                [
                    html.Iframe(
                        srcDoc=final.to_html(),
                        style={
                            "border-width": "0",
                            "width": "100%",
                            "height": "400px",
                        },
                    )
                ],
            ),
        ],
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Iframe(
                        srcDoc=lineplot.to_html(),
                        style={
                            "border-width": "0",
                            "width": "100%",
                            "height": "400px",
                        },
                    )
                ]
            )
        ]
    ),
]


app = Dash("Vancouver Crime Dashboard")

# Load data
van_crime = pd.read_csv("data/processed_merged_df.csv")

"""Options"""
# Options for neighbourhood
opt_dropdown_neighbourhood = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in np.unique(data["NEIGHBOUTHOOD"])
]

# Options for year
opt_slider_year = [
    {"label": year, "value": year} for year in np.unique(van_crime["YEAR"])
]

opt_dropdown_time = [
    {"label": "Day", "value": "Time"},
    {"label": "Night", "value": "Time"},
    {"label": "Day and Night", "value": "Time"},
]

"""Card"""
# Card
card = [
    dbc.Card(
        [
            html.H2("", className="card-title"),  # need to fill in the data
            html.P("Total Number of Crimes", className="card-text"),
        ],
        body=True,
        color="light",
    )
]

""" Layouts """
filter_panel = [
    ### Top Header Text
    html.H2("Vancouver Crime Dashboard"),
    html.Br(),
    html.Br(),
    ### Card
    card,
    html.H3("Filters", className="text-primary"),
    html.H5("Neighbourhood", className="text-dark"),
    dcc.Dropdown(
        id="neighbourhood_input",
        value="Kitsilano",
        options=opt_dropdown_neighbourhood,
        className="dropdown",
    ),
    html.Br(),
    ### Slider for year
    html.H5("Year", className="text-dark"),
    dcc.Slider(2017, 2021, 1, value=2021, id="year_slider"),
    html.Br(),
    html.H5("Time", className="text-dark"),
    dcc.Dropdown(
        id="time_input",
        value="Day and night",
        options=opt_dropdown_time,
        className="dropdown",
    ),
]

"""Layout"""
# Define page layout
page_layout = html.Div(
    className="page_layout",
    children=[
        dbc.Col(filter_panel, className="panel"),
        dbc.Col(plot_body, className="body"),
    ],
)

# Overall layout
app.layout = html.Div(id="main", className="app", children=page_layout)


if __name__ == "__main__":
    app.run_server(debug=True)
