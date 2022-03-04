import altair as alt
import pandas as pd
import utm
import geopandas as gpd
import numpy as np
from prep_data import prep_data


def load_nb():
    nb = pd.read_csv(r'../data/van_neighbourhoods.csv',sep=";")
    nb['geo_point_2d']= nb["geo_point_2d"].apply(lambda x:
                                             np.fromstring(x, dtype=np.double, sep=','))
    nb[['nb_lat','nb_lon']] = pd.DataFrame(nb["geo_point_2d"].to_list(), columns=['nb_lat', 'nb_lon'])
    nb = nb.rename(columns={'Name': 'Neighborhood'})
    nb.loc[nb.Neighborhood == "Arbutus-Ridge", "Neighborhood"] = "Arbutus Ridge"
    nb.loc[nb.Neighborhood == "Downtown", "Neighborhood"] = "Central Business District"
    return nb[["Neighborhood","nb_lat","nb_lon"]]


def load_gdf():
    gdf = gpd.read_file("../data/van_spatial_data")
    return  gdf


def prep_map_data(df, nbs=[], yrs=[]):
    # filters dataset by neighbourhood/ years and add geo coordenates
    # load coordenates of Van neighborhoods
    van_nb = load_nb()
    if nbs:
        df = df[df.Neighborhood.isin(nbs)]
    if yrs:
        df = df[df.YEAR.isin(yrs)]
    # group by Neighborhood (default = all neighborhoods)
    df_filtered = df.groupby("Neighborhood").size().reset_index(name='Crimes')
    # add centre geo coordenates for each neighbourhood
    df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")
    return df_filtered


def plot_map(df, nbs=[], yrs=[]):
    # load Van map
    gdf = load_gdf()

    # load coordenates of Van neighborhoods
    van_nb = load_nb()

    # filters dataset by neighbourhood/ years and add geo coordenates
    if nbs:
        df = df[df.Neighborhood.isin(nbs)]
    if yrs:
        df = df[df.YEAR.isin(yrs)]
    # group by Neighborhood (default = all neighborhoods)
    df_filtered = df.groupby("Neighborhood").size().reset_index(name='Crimes')
    # add centre geo coordenates for each neighbourhood
    df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")

    base = alt.Chart(gdf).mark_geoshape(
        stroke='gray', 
        fill=None
    )

    pts = alt.Chart(df_filtered).mark_circle().encode(
        latitude='nb_lat',
        longitude='nb_lon',
        size='Crimes',
        color=alt.Color('Crimes', scale=alt.Scale(scheme='yelloworangered')),
        tooltip=["Neighborhood","Crimes"]
    )
    
    return base + pts


def plot_map_all():
    # load Van crime data
    filename = "../data/processed/merged_df.csv"
    df = pd.read_csv(filename,  index_col=0)
    df = prep_data(df)
    
    # load Van map
    gdf = load_gdf()

    # load coordenates of Van neighborhoods
    van_nb = load_nb()

    # group by Neighborhood (default = all neighborhoods)
    df_filtered = df.groupby("Neighborhood").size().reset_index(name='Crimes')
    # add centre geo coordenates for each neighbourhood
    df_filtered = pd.merge(df_filtered, van_nb, on="Neighborhood")

    base = alt.Chart(gdf).mark_geoshape(
        stroke='gray', 
        fill=None
    )

    pts = alt.Chart(df_filtered).mark_circle().encode(
        latitude='nb_lat',
        longitude='nb_lon',
        size='Crimes',
        color=alt.Color('Crimes', scale=alt.Scale(scheme='yelloworangered')),
        tooltip=["Neighborhood","Crimes"]
    )
    
    return base + pts