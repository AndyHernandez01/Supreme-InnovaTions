import streamlit as st
import json
import requests


st.title("Biosure WDS monitoring")
Location_options = requests.get(url = "http://0.0.0.0:8000/api/v1/items/loc").json()
locations = ['']
locations.extend([*set(l['location'] for l in Location_options)])
option = st.selectbox('What device would you like to check today (location): ', locations)



if st.button('Search'):
    res = requests.get(url = f"http://0.0.0.0:8000/api/v1/items/?skip=0&limit=100&search{option}")
    st.json(res.text)
