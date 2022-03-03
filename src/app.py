from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import dash_daq as daq


app = Dash("Vancouver Crime Dashboard")

# Load data
van_crime = pd.read_csv("data/processed_merged_df.csv")

"""Options"""
# Options for neighbourhood
opt_dropdown_neighbourhood = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in np.unique(van_crime["NEIGHBOUTHOOD"])
]

# Options for year
opt_slider_year = [
    {"label": year, "value": year}
    for year in np.unique(van_crime["YEAR"])
]

opt_dropdown_time = [
    {"label": "Day", "value": "Time"},
    {"label": "Night", "value": "Time"},
    {"label": "Day and Night", "value" : "Time"}
]

"""Card"""
# Card
card = [
    dbc.Card(
        [
        html.H2("", className="card-title"), #need to fill in the data
        html.P("Total Number of Crimes", className="card-text")
        ],
        body=True,
        color="light"
)]

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
    dcc.Slider(2017, 2021, 1,
        value=2021,
        id="year_slider"
        ),
    html.Br(),

    html.H5("Time", className="text-dark"),
    dcc.Dropdown(
        id="time_input",
        value="Day and night",
        options=opt_dropdown_time,
        className="dropdown",
    )
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


if __name__ == '__main__':
    app.run_server(debug=True)
