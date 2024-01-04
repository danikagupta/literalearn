import streamlit as st
import requests
import pandas as pd

sheet_mapping={
    "users": "https://v1.nocodeapi.com/gprof/google_sheets/ULJTWlUlxDbMDOzR",
    "sentences": "https://v1.nocodeapi.com/gprof/google_sheets/UXWnqHbJxMezIpoE",
    "status": "https://v1.nocodeapi.com/gprof/google_sheets/JozQVcMxjnDpkeAF",
}

sheets=sheet_mapping.keys()


def get_sheet(sheet,debugging=False):

    url=sheet_mapping[sheet]
    params = {"tabId": 'Sheet1'}
    r = requests.get(url = url, params = params)
    # print(f"R={r}")
    result = r.json()
    # print(f"Result={result}")
    d=result['data']
    # print(f"Result Data={d}")
    df=pd.DataFrame(d)
    if debugging:
        print(result)
        st.dataframe(df)
    return df

def add_to_sheet(sheet,row,debugging=False):
    if debugging:
        print(f"DataStore.AddToSheet: Adding {row} to {sheet}") 
    url=sheet_mapping[sheet]
    params = {"tabId": "Sheet1"}
    data=[row]
    r = requests.post(url = url, params = params, json = data)
    result = r.json()
    if debugging:
        print(result)   
    return result

def show_sheets():
    st.write("Sheets:")
    for sheet in sheets:
        df=get_sheet(sheet)
        st.write(f"## {sheet}")
        st.dataframe(df)

