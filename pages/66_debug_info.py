import streamlit as st
import requests

import datastore
import cookiestore

import pandas as pd

st.write("# Session state")
df = pd.DataFrame(list(st.session_state.items()), columns=['Key', 'Value'], index=None)
st.dataframe(df,hide_index=True)
st.write(f"Session state: {st.session_state}")

cookiestore.cookie_ui()

datastore.show_sheets()

if st.button("Remove query params"):
    cookiestore.remove_query_params()