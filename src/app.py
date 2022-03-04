from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import utm
import geopandas as gpd
from prep_data import prep_data

alt.data_transformers.disable_max_rows()

# read the data
data = pd.read_csv("data/processed/processed_df.csv", index_col=0)


app = Dash(
    __name__,
    title="Vancouver Crime Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server

"""Options"""
# Options for neighbourhood
opt_dropdown_neighbourhood = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in data["Neighborhood"].dropna().unique()
]

opt_dropdown_time = [
    {"label": "Day", "value": "Day"},
    {"label": "Night", "value": "Night"},
    {"label": "Day and Night", "value": "Day and Night"},
]

"""Card"""
# Cards
card1 = dbc.Card(
    [
        html.H4(
            "Total Number of Crimes", className="card-title", style={"marginLeft": 50}
        ),
        html.Div(
            id="summary", style={"color": "#E33B18", "fontSize": 25, "marginLeft": 140}
        ),
    ],
    style={"width": "25rem", "marginLeft": 20},
    body=True,
    color="light",
)

card2 = dbc.Card(
    [
        html.H5("Neighbourhood", className="text-dark"),
        dcc.Dropdown(
            id="neighbourhood_input",
            value="Kitsilano",
            options=opt_dropdown_neighbourhood,
            className="dropdown",
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        ### Slider for year
        html.H5("Year", className="text-dark"),
        dcc.Slider(
            2017,
            2021,
            1,
            value=2021,
            id="year_slider",
            marks={
                2017: "2017",
                2018: "2018",
                2019: "2019",
                2020: "2020",
                2021: "2021",
            },
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H5("Time", className="text-dark"),
        dcc.Dropdown(
            id="time_input",
            value="Day and Night",
            options=opt_dropdown_time,
            className="dropdown",
        ),
    ],
    style={"width": "25rem", "marginLeft": 20},
    body=True,
    color="light",
)

""" Layouts """
filter_panel = [
    ### Top Header Text
    html.H2("Vancouver Crime Dashboard", style={"marginLeft": 20}),
    html.Br(),
    html.Br(),
    ### Cards
    card1,
    html.Br(),
    html.Br(),
    html.H4("Filters", style={"marginLeft": 20}),
    card2,
    html.Br(),
]


plot_body = [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Iframe(
                        id="bar_plot",
                        className="bar_plot",
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
                        id="map_plot",
                        className="map_plot",
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
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Iframe(
                        id="line_plot",
                        className="line_plot",
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

# Define page layout
page_layout = html.Div(
    className="page_layout",
    children=[
        dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col(filter_panel, className="panel", width=3),
                dbc.Col(plot_body, className="body"),
            ]
        ),
    ],
)

# Overall layout
app.layout = html.Div(id="main", className="app", children=page_layout)


# Functions
def load_nb():
    nb = pd.read_csv(r"data/van_neighbourhoods.csv", sep=";")
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


def load_gdf():
    gdf = gpd.read_file("data/van_spatial_data")
    return gdf


@app.callback(
    Output("map_plot", "srcDoc"),
    Input("year_slider", "value"),
)
def plot_map_all(year):
    # load Van crime data
    filename = "data/processed/merged_df.csv"
    df = pd.read_csv(filename, index_col=0)
    df = prep_data(df)

    # load Van map
    gdf = load_gdf()

    # load coordenates of Van neighborhoods
    van_nb = load_nb()

    # filter by year
    df = df[df.YEAR == year]
    # group by Neighborhood
    df_filtered = df.groupby("Neighborhood").size().reset_index(name="Crimes")
    # add centre geo coordenates for each neighbourhood
    df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")

    base = alt.Chart(gdf).mark_geoshape(stroke="gray", fill=None)

    pts = (
        alt.Chart(df_filtered, title="Number of Crimes per Neighbourhood")
        .mark_circle()
        .encode(
            latitude="nb_lat",
            longitude="nb_lon",
            size="Crimes",
            color=alt.Color("Crimes", scale=alt.Scale(scheme="yelloworangered")),
            tooltip=["Neighborhood", "Crimes"],
        )
    )

    return (base + pts).configure_title(fontSize=20).to_html()


@app.callback(
    Output("line_plot", "srcDoc"),
    Input("time_input", "value"),
    Input("neighbourhood_input", "value"),
)
def lineplot(time, neighbourhood):
    data = pd.read_csv("data/processed/merged_df.csv", index_col=0)
    data = data[data["NEIGHBOURHOOD"] == neighbourhood]

    if time == "Day and Night":
        lineplot = (
            alt.Chart(data, title="Crimes over Time")
            .mark_line()
            .encode(
                x=alt.X("YEAR:O", title="Year"),
                y=alt.Y("count(HOUR)", title="Number of Crimes"),
                color=alt.Color(
                    "TIME", scale=alt.Scale(scheme="yelloworangered"), title="Time"
                ),
            )
            .configure_axis(labelFontSize=14, titleFontSize=16)
            .configure_legend(
                titleFontSize=16,
                orient="top-right",
                fillColor="#EEEEEE",
                strokeColor="gray",
                cornerRadius=10,
                padding=10,
                labelFontSize=16,
            )
            .configure_title(fontSize=20)
            .properties(width=1000, height=300)
        )

    elif time == "Day":
        data = data[data["TIME"] == "day"]
        lineplot = (
            alt.Chart(data, title="Crimes over Time")
            .mark_line()
            .encode(
                x=alt.X("YEAR:O", title="Year"),
                y=alt.Y("count(HOUR)", title="Number of Crimes"),
                color=alt.Color(
                    "TIME", scale=alt.Scale(scheme="yelloworangered"), title="Time"
                ),
            )
            .configure_axis(labelFontSize=14, titleFontSize=16)
            .configure_legend(
                titleFontSize=16,
                orient="top-right",
                fillColor="#EEEEEE",
                strokeColor="gray",
                cornerRadius=10,
                padding=10,
                labelFontSize=16,
            )
            .configure_title(fontSize=20)
            .properties(width=1000, height=300)
        )

    else:
        data = data[data["TIME"] == "night"]
        lineplot = (
            alt.Chart(data, title="Crimes over Time")
            .mark_line()
            .encode(
                x=alt.X("YEAR:O", title="Year"),
                y=alt.Y("count(HOUR)", title="Number of Crimes"),
                color=alt.Color(
                    "TIME", scale=alt.Scale(scheme="yelloworangered"), title="Time"
                ),
            )
            .configure_axis(labelFontSize=14, titleFontSize=16)
            .configure_legend(
                titleFontSize=16,
                orient="top-right",
                fillColor="#EEEEEE",
                strokeColor="gray",
                cornerRadius=10,
                padding=10,
                labelFontSize=16,
            )
            .configure_title(fontSize=20)
            .properties(width=1000, height=300)
        )

    return lineplot.to_html()


@app.callback(
    Output("bar_plot", "srcDoc"),
    Input("neighbourhood_input", "value"),
    Input("year_slider", "value"),
)
def barchart(neighbourhood, year):
    data = pd.read_csv("data/processed/merged_df.csv", index_col=0)
    data = data[data["YEAR"] == year]
    data = data[data["NEIGHBOURHOOD"] == neighbourhood]
    data = pd.DataFrame(
        data=data[["YEAR", "TYPE"]].value_counts(), columns=["COUNTS"]
    ).reset_index(level=["YEAR", "TYPE"])

    barchart = (
        alt.Chart(data, title="Crimes by Type")
        .mark_bar()
        .encode(
            x=alt.X(
                "TYPE", sort="-y", axis=alt.Axis(labels=False), title="Type of Crime"
            ),
            y=alt.Y("COUNTS", title="Number of Crimes"),
            color=alt.Color(
                "TYPE", scale=alt.Scale(scheme="yelloworangered"), title="Type"
            ),
            tooltip=alt.Tooltip("TYPE"),
        )
        .transform_window(
            rank="rank(COUNTS)", sort=[alt.SortField("COUNTS", order="descending")]
        )
        .transform_filter((alt.datum.rank < 15))
        .configure_axis(labelFontSize=14, titleFontSize=16)
        .configure_legend(titleFontSize=14)
        .configure_title(fontSize=20)
        .properties(width=300, height=300)
    )
    return barchart.to_html()


@app.callback(
    Output("summary", "children"),
    Input("neighbourhood_input", "value"),
    Input("year_slider", "value"),
)
def summary(neighbourhood, year):
    data = pd.read_csv("data/processed/merged_df.csv", index_col=0)
    data = data[data["YEAR"] == year]
    data = data[data["NEIGHBOURHOOD"] == neighbourhood]
    return len(data)


if __name__ == "__main__":
    app.run_server(debug=True)
