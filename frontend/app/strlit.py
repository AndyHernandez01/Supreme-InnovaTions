import streamlit as st
import json
import requests

@st.cache_resource
def get_data():
    return requests.get(url = "http://0.0.0.0:8000/api/v1/items/loc").json()

st.title("Biosure WDS monitoring")
Location_options = get_data()
locations = ['']
locations.extend([*set(l['location'] for l in Location_options)])
option = st.selectbox('What device would you like to check today (location): ', locations)

if st.button('Search'):
    res = requests.get(url = f"http://0.0.0.0:8000/api/v1/items/?skip=0&limit=100&search={option}")
    st.json(res.text)

"""Create live analytics dashboard for Biosure WDS devices"""
live_dashboard = st.container()
with live_dashboard:
    st.title("Live Dashboard")
    st.text("This is a live dashboard for Biosure WDS devices")
    #collect data from API
    #display data in a table
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Device Status")
        #display data in a graph
    with col2:
        st.subheader("Device Status")
    
    #display data in a graph
