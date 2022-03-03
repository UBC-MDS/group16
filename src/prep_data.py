import altair as alt
import pandas as pd
import utm
import geopandas as gpd
import numpy as np


def prep_data(df):
    # eliminate data sets without coordenates
    df = df[df["HUNDRED_BLOCK"]!='OFFSET TO PROTECT PRIVACY']
    df.reset_index(drop=True, inplace=True)
    # rename columns
    df = df.rename(columns={'NEIGHBOURHOOD': 'Neighborhood', 'TYPE': 'Type'})
    # convert coordenates
    pp_df = df.copy()
    pp_df.loc[:,"lat"], pp_df.loc[:,"lon"] = utm.to_latlon(pp_df["X"], pp_df["Y"], 10, 'n', strict=False)
    return pp_df