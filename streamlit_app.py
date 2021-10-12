# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from PIL import Image


# SETTING PAGE CONFIG TO WIDE MODE

st.set_page_config(layout="wide")
st.title("By Thanapol Kuharungroj 6130811321")

# SETTING Sidebar
st.sidebar.header("Please select here")
date_select = st.sidebar.selectbox("Date Selection",("1-Jan-2019", "2-Jan-2019","3-Jan-2019","4-Jan-2019","5-Jan-2019"))
hour_selected = st.sidebar.slider("Select hour of travelling", 0, 23)

# LAYING OUT THE TOP SECTION

st.text(
"""

Showing the number of travelling started for Bangkok.
By sliding and selecting date.

""")


timedisplay = "Date Displayed : " + date_select
st.title(timedisplay)


# LOADING DATA
DATE_TIME = "date/time"
DATA_DAY1 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv")
DATA_DAY2 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv")
DATA_DAY3= ("https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv")
DATA_DAY4 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv")
DATA_DAY5 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv")

#SELECT DATA ACCORDING TO date_select
if date_select == "1-Jan-2019" :
  DATA_URL = DATA_DAY1
elif date_select == "2-Jan-2019" :
  DATA_URL = DATA_DAY2
elif date_select == "3-Jan-2019" :
  DATA_URL = DATA_DAY3
elif date_select == "4-Jan-20199" :
  DATA_URL = DATA_DAY4
elif date_select == "5-Jan-2019" :
  DATA_URL = DATA_DAY5

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data = data[['timestart','latstartl','lonstartl']].copy()
    data = data.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

##################################################################################
##################################################################################
# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))
    
##################################################################################
##################################################################################
# FILTERING DATA BY HOUR SELECTED
data = data[(data[DATE_TIME].dt.hour == hour_selected) & (data[DATE_TIME].dt.year == 2019)]


# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS


# SETTING THE ZOOM LOCATIONS
zoom_level = 10

midpoint = [13.774646978946686, 100.62422280542049]

map(data, midpoint[0], midpoint[1], zoom_level)
st.write("Diagram for route using at time selected")


# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "Start travel location": hist})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.altair_chart(alt.Chart(chart_data)
          .mark_area(
              interpolate='step-after',
          ).encode(
              x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
              y=alt.Y("Start travel location:Q"),
              tooltip=['minute', 'Start travel location']
          ).configure_mark(
              opacity=0.5,
              color='red'
          ), use_container_width=True)