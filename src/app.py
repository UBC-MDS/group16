from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import utm
import geopandas as gpd

alt.data_transformers.disable_max_rows()

# read the data
data = pd.read_csv("data/processed/processed_df.csv", index_col=0)


app = Dash(
    __name__,
    title="Vancouver Crime Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server


# def prep_data(df):
#     # eliminate data sets without coordenates
#     df = df[df["HUNDRED_BLOCK"] != "OFFSET TO PROTECT PRIVACY"]
#     df.reset_index(drop=True, inplace=True)
#     # rename columns
#     df = df.rename(columns={"NEIGHBOURHOOD": "Neighborhood", "TYPE": "Type"})
#     # convert coordenates
#     pp_df = df.copy()
#     pp_df.loc[:, "lat"], pp_df.loc[:, "lon"] = utm.to_latlon(
#         pp_df["X"], pp_df["Y"], 10, "n", strict=False
#     )
#     return pp_df


# def load_nb():
#     nb = pd.read_csv(r"../data/van_neighbourhoods.csv", sep=";")
#     nb["geo_point_2d"] = nb["geo_point_2d"].apply(
#         lambda x: np.fromstring(x, dtype=np.double, sep=",")
#     )
#     nb[["nb_lat", "nb_lon"]] = pd.DataFrame(
#         nb["geo_point_2d"].to_list(), columns=["nb_lat", "nb_lon"]
#     )
#     nb = nb.rename(columns={"Name": "Neighborhood"})
#     nb.loc[nb.Neighborhood == "Arbutus-Ridge", "Neighborhood"] = "Arbutus Ridge"
#     nb.loc[nb.Neighborhood == "Downtown", "Neighborhood"] = "Central Business District"
#     return nb[["Neighborhood", "nb_lat", "nb_lon"]]


# def load_gdf():
#     gdf = gpd.read_file("../data/van_spatial_data")
#     return gdf


# def prep_map_data(df, nbs=[], yrs=[]):
#     # filters dataset by neighbourhood/ years and add geo coordenates
#     # load coordenates of Van neighborhoods
#     van_nb = load_nb()
#     if nbs:
#         df = df[df.Neighborhood.isin(nbs)]
#     if yrs:
#         df = df[df.YEAR.isin(yrs)]
#     # group by Neighborhood (default = all neighborhoods)
#     df_filtered = df.groupby("Neighborhood").size().reset_index(name="Crimes")
#     # add centre geo coordenates for each neighbourhood
#     df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")
#     return df_filtered


# def plot_map(df, nbs=[], yrs=[]):
#     # load Van map
#     gdf = load_gdf()

#     # load coordenates of Van neighborhoods
#     van_nb = load_nb()

#     # filters dataset by neighbourhood/ years and add geo coordenates
#     if nbs:
#         df = df[df.Neighborhood.isin(nbs)]
#     if yrs:
#         df = df[df.YEAR.isin(yrs)]
#     # group by Neighborhood (default = all neighborhoods)
#     df_filtered = df.groupby("Neighborhood").size().reset_index(name="Crimes")
#     # add centre geo coordenates for each neighbourhood
#     df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")

#     base = alt.Chart(gdf).mark_geoshape(stroke="gray", fill=None)

#     pts = (
#         alt.Chart(df_filtered)
#         .mark_circle()
#         .encode(
#             latitude="nb_lat",
#             longitude="nb_lon",
#             size="Crimes",
#             color=alt.Color("Crimes", scale=alt.Scale(scheme="yelloworangered")),
#             tooltip=["Neighborhood", "Crimes"],
#         )
#     )

#     return (base + pts).to_html()


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
# Card
card = dbc.Card(
    [
        html.H4("Total Number of Crimes", className="card-title"),
        html.Div(id="summary", style={"color": "red", "fontSize": 20}),
    ],
    style={"width": "18rem"},
    body=True,
    color="light",
)

""" Layouts """
filter_panel = [
    ### Top Header Text
    html.H2("Vancouver Crime Dashboard"),
    html.Br(),
    html.Br(),
    ### Card
    card,
    html.Br(),
    html.Br(),
    html.H3("Filters", className="text-primary"),
    html.Br(),
    html.H5("Neighbourhood", className="text-dark"),
    dcc.Dropdown(
        id="neighbourhood_input",
        value="Kitsilano",
        options=opt_dropdown_neighbourhood,
        className="dropdown",
    ),
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
        marks={2017: "2017", 2018: "2018", 2019: "2019", 2020: "2020", 2021: "2021"},
    ),
    html.Br(),
    html.Br(),
    html.H5("Time", className="text-dark"),
    dcc.Dropdown(
        id="time_input",
        value="Day and Night",
        options=opt_dropdown_time,
        className="dropdown",
    ),
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
            # dbc.Col(
            #     [
            #         html.Iframe(
            #             srcDoc=final.to_html(),
            #             style={
            #                 "border-width": "0",
            #                 "width": "100%",
            #                 "height": "400px",
            #             },
            #         )
            #     ],
            # ),
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
        dbc.Row(
            [
                dbc.Col(filter_panel, className="panel", width=4),
                dbc.Col(plot_body, className="body"),
            ]
        )
    ],
)

# Overall layout
app.layout = html.Div(id="main", className="app", children=page_layout)


# Functions
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
            .properties(width=700, height=200)
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
            .properties(width=700, height=200)
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
            .properties(width=700, height=200)
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
        )
        .transform_window(
            rank="rank(COUNTS)", sort=[alt.SortField("COUNTS", order="descending")]
        )
        .transform_filter((alt.datum.rank < 15))
        .properties(width=200, height=200)
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
