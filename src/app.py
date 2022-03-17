from dash import Dash, html, Input, Output, dcc, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd

alt.data_transformers.disable_max_rows()

# Read the data
data = pd.read_csv("data/processed/processed_df.csv", index_col=0)

# App server
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
opt_dropdown_neighbourhood.remove(opt_dropdown_neighbourhood[-1])
opt_dropdown_neighbourhood.remove(opt_dropdown_neighbourhood[-4])

# Options for time
opt_dropdown_time = [
    {"label": "Day", "value": "Day"},
    {"label": "Night", "value": "Night"},
    {"label": "Day and Night", "value": "Day and Night"},
]

# Options for year
opt_radio_year = [
    {"label": "2017", "value": 2017},
    {"label": "2018", "value": 2018},
    {"label": "2019", "value": 2019},
    {"label": "2020", "value": 2020},
    {"label": "2021", "value": 2021},
]

# Collapse button
collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={
                "margin-top": "10px",
                "width": "150px",
                "background-color": "#E33B18",
                "color": "white",
            },
        ),
    ]
)

"""Cards"""
# Summary card
card1 = dbc.Card(
    [
        # Summary statistics
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

# Filters card
card2 = dbc.Card(
    [
        # Dropdown for neighbourhood
        html.H5("Neighbourhood", className="text-dark"),
        dcc.Dropdown(
            id="neighbourhood_input",
            value=["Kitsilano"],
            options=opt_dropdown_neighbourhood,
            className="dropdown",
            multi=True,
        ),
        html.Br(),
        # Radio button for year
        html.H5("Year", className="text-dark"),
        dcc.RadioItems(
            id="year_radio",
            value=2021,
            options=opt_radio_year,
            className="radiobutton",
            labelStyle={"display": "in-block", "marginLeft": 20},
        ),
        html.Br(),
        # Dropdown for time
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

# information
card3 = dbc.Card(
    [
        html.H5("Information", className="text-dark"),
        html.P(
            [
                "Data used in this dashboard is sourced from ",
                dcc.Link(
                    "Vancouver Police Department",
                    href="https://geodash.vpd.ca/opendata/",
                    target="_blank",
                ),
                " (It has been filtered to only include incidents with location data from 2017 to 2021.)",
            ]
        ),
    ],
    style={"width": "25rem", "marginLeft": 20},
    body=True,
    color="light",
)

"""Layouts"""
# Filter layout
filter_panel = [
    dbc.Row(
        [
            html.H2("Vancouver Crime Dashboard", style={"marginLeft": 20}),
            dbc.Collapse(
                html.P(
                    """
                The filter panel below helps you filter the plots. The neighborhood filter can accept multiple options and 
                updates the bar chart and the line graph. The year filter will update the bar chart and the map so they 
                show the crimes for the year specified. The time filter which has three options will aggregate the line graph 
                by time of the day. The summary card represents the number of crimes for the specified year and neighbourhood.""",
                    style={"marginLeft": 20},
                ),
                id="collapse",
            ),
        ]
    ),
    dbc.Row([collapse], style={"marginLeft": 120}),
    html.Br(),
    card1,
    html.Br(),
    html.H4("Filters", style={"marginLeft": 20}),
    card2,
    html.Br(),
    card3,
]

# Plots layout
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

# Page layout
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


"""Functions"""

@app.callback(
    Output("map_plot", "srcDoc"),
    Input("year_radio", "value"),
)
def plot_map_all(year):
    url = "https://raw.githubusercontent.com/UBC-MDS/vancouver_crime_dashboard/main/data/van_nb.geojson"
    geoj = alt.Data(url=url, format=alt.DataFormat(property="features", type="json"))
    df = pd.read_csv(r"data/processed/processed_df.csv")
    df = df[df.YEAR == year] 
    df = df[df["HUNDRED_BLOCK"] != "OFFSET TO PROTECT PRIVACY"]
    df = df.rename(columns={"NEIGHBOURHOOD": "Neighborhood", "TYPE": "Type"})
    df = df.groupby("Neighborhood").size().reset_index(name="Crimes")
    base = (
        alt.Chart(geoj)
        .mark_geoshape(fill=None)
        .project(type="identity", reflectY=True)
    )
    pts = (
        base
        + alt.Chart(df, title="Number of Crimes per Neighbourhood")
        .transform_lookup(
            default="0",
            as_="geo",
            lookup="Neighborhood",
            from_=alt.LookupData(data=geoj, key="properties.name"),
        )
        .mark_geoshape()
        .encode(
            alt.Color(
                "Crimes",
                scale=alt.Scale(scheme="yelloworangered"),
                legend=alt.Legend(orient="right", title="Crimes"),
            ),
            alt.Shape(field="geo", type="geojson"),
            tooltip=["Crimes", "Neighborhood:N"],
        )
    ).project(type="identity", reflectY=True)
    map = (
        (base + pts)
        .configure_title(fontSize=20)
        .configure_legend(
            titleFontSize=16,
            labelFontSize=14,
        )
    )

    return map.to_html()  
"""def plot_map_all(year):
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

    map = (
        (base + pts)
        .configure_title(fontSize=20)
        .configure_legend(
            titleFontSize=16,
            labelFontSize=14,
        )
    )
    return map.to_html()
"""

@app.callback(
    Output("line_plot", "srcDoc"),
    Input("time_input", "value"),
    Input("neighbourhood_input", "value"),
)
def lineplot(time, neighbourhood):
    data = pd.read_csv("data/processed/processed_df.csv", index_col=0)
    data = data[data.Neighborhood.isin(neighbourhood)]

    if time == "Day":
        data = data[data["TIME"] == "day"]

    elif time == "Night":
        data = data[data["TIME"] == "night"]

    line_plot = (
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
            labelFontSize=14,
        )
        .configure_title(fontSize=20)
        .properties(width=1000, height=300)
    )

    return line_plot.to_html()


@app.callback(
    Output("bar_plot", "srcDoc"),
    Input("neighbourhood_input", "value"),
    Input("year_radio", "value"),
)
def barchart(neighbourhood, year):
    data = pd.read_csv("data/processed/processed_df.csv", index_col=0)
    data = data[data["YEAR"] == year]
    data = data[data.Neighborhood.isin(neighbourhood)]
    data = pd.DataFrame(
        data=data[["YEAR", "Type"]].value_counts(), columns=["Counts"]
    ).reset_index(level=["YEAR", "Type"])

    barchart = (
        alt.Chart(data, title="Crimes by Type")
        .mark_bar()
        .encode(
            y=alt.Y(
                "Type", sort="-x", axis=alt.Axis(labels=False), title="Type of Crime"
            ),
            x=alt.Y("Counts", title="Number of Crimes"),
            color=alt.Color(
                "Type", scale=alt.Scale(scheme="yelloworangered"), title="Type"
            ),
            tooltip=alt.Tooltip(["Type", "Counts"]),
        )
        .transform_window(
            rank="rank(COUNTS)", sort=[alt.SortField("COUNTS", order="descending")]
        )
        .transform_filter((alt.datum.rank < 15))
        .configure_axis(labelFontSize=14, titleFontSize=16)
        .configure_legend(
            titleFontSize=16,
            labelFontSize=14,
        )
        .configure_title(fontSize=20)
        .properties(width=300, height=300)
    )
    return barchart.to_html()


@app.callback(
    Output("summary", "children"),
    Input("neighbourhood_input", "value"),
    Input("year_radio", "value"),
)
def summary(neighbourhood, year):
    data = pd.read_csv("data/processed/processed_df.csv", index_col=0)
    data = data[data["YEAR"] == year]
    data = data[data.Neighborhood.isin(neighbourhood)]
    return len(data)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
