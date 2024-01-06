import streamlit as st
import requests

import datastore
import cookiestore

import pandas as pd

ee=st.button("Enable English")
if ee:
    datastore.enable_english("google-111998729756733250236","test",True)

df=datastore.get_questions("en",10,True)
st.dataframe(df,hide_index=True)

st.write("# Session state")
df = pd.DataFrame(list(st.session_state.items()), columns=['Key', 'Value'], index=None)
st.dataframe(df,hide_index=True)
st.write(f"Session state: {st.session_state}")

cookiestore.cookie_ui()

datastore.show_sheets()
