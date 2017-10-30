# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 11:56:42 2017

@author: Agnes
"""

import plotly.plotly as py
import pandas as pd

# prepare df in nsf_descriptive.py
df = award_by_state.sum().loc[2017]
text = df.index.get_level_values(1)+'<br>$'+(df/1e6).round(decimals=2).astype(str)+'M'\
    +'<br>Count: '+award_by_state.count().loc[2017].astype(str)
df = pd.DataFrame({'amount':df.values/1e6, 'text':text, 'state':df.index.get_level_values(1), 'code':df.index.get_level_values(0)})

data = [ dict(
        type='choropleth',
        autocolorscale = True,
        locations = df.code,
        z = df.amount,
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Millions USD")
        ) ]

layout = dict(
        title = '2017 NSF Award Amount by State<br>(Hover for amount)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
py.iplot( fig, filename='nsf-2017-map' )