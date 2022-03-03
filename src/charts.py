import altair as alt
import numpy as np
import pandas as pd
from altair_data_server import data_server


def lineplot(df):
    alt.data_transformers.enable('data_server')
    alt.renderers.enable('mimetype')
    lineplot = alt.Chart(df).mark_line().encode(
        x=alt.X("YEAR:O", title='Year'),
        y=alt.Y('count(HOUR)', scale=alt.Scale(domain = [13000, 28000])),
        color=alt.Color('TIME', 
                        scale=alt.Scale(scheme='yelloworangered'),
                        title='Time')
    ).properties(
        width=500,
        height=200)
    return lineplot

def barchart(df):
    alt.data_transformers.enable('data_server')
    alt.renderers.enable('mimetype')
    data = pd.DataFrame(data=df[['YEAR', 'TYPE']].value_counts(),
                        columns=['COUNTS']).reset_index(level=['YEAR', 'TYPE'])
    barchart = alt.Chart(data).mark_bar().encode(
        x = alt.X('TYPE', sort='-y',
                  axis=alt.Axis(labels=False)),
        y = alt.Y('COUNTS'),
        color=alt.Color('TYPE',
                        scale=alt.Scale(scheme='yelloworangered'),
                        title='Type')
    ).transform_window(
        rank='rank(COUNTS)',
        sort=[alt.SortField('COUNTS', order='descending')]
    ).transform_filter(
        (alt.datum.rank < 15)
    ).properties(
        width=200,
        height=200)
    return barchart