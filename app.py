import streamlit as st
import time
import numpy as np
import requests
import pandas as pd
import requests
import datetime

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource


#default_value_goes_here = 'TSLA'
#user_input = st.text_input("label goes here", default_value_goes_here)

ticker = st.sidebar.text_input("Ticker",'TSLA')

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=HBC0CDPGC19N0YML'
r = requests.get(url)
data = r.json()
df1 = pd.DataFrame(data["Time Series (Daily)"])

for_pandas =[]

dates = list(data['Time Series (Daily)'].keys())


for date in dates:
    for_pandas.append({'date':date,
                       'open':data['Time Series (Daily)'][date]['1. open'],
                       'high':data['Time Series (Daily)'][date]['2. high'],
                       'low':data['Time Series (Daily)'][date]['3. low'],
                       'close':data['Time Series (Daily)'][date]['4. close'],
                       'volume':data['Time Series (Daily)'][date]['5. volume']})

df1 = pd.DataFrame(for_pandas)
#df1 = df1.set_index('date')

status_text = st.sidebar.empty()

x = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in df1['date']]
y= df1['close'].tolist()
select_tools = ['pan', 'zoom_in', 'zoom_out', 'reset']

# Create a figure 
fig = figure(title= ticker +' Closing Prices',
             plot_height=300, plot_width=300, x_axis_type='datetime',
             toolbar_location='right', tools = select_tools)

# Draw the coordinates as circles
fig.line(x, 
         y,
         color='green',
         line_width=3, 
         alpha=0.5)
# configure so that Bokeh chooses what (if any) scroll tool is active
fig.toolbar.active_scroll = "auto"



st.bokeh_chart(fig)


#st.button("Re-run")


