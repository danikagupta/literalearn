import streamlit as st
import requests
import pandas as pd

sheet_mapping={
    "users": "https://v1.nocodeapi.com/gprof/google_sheets/ULJTWlUlxDbMDOzR",
    "sentences": "https://v1.nocodeapi.com/gprof/google_sheets/UXWnqHbJxMezIpoE",
    "status": "https://v1.nocodeapi.com/gprof/google_sheets/JozQVcMxjnDpkeAF",
}

sheets=sheet_mapping.keys()


def get_sheet(sheet,debugging):

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

def get_user_row(subId,debugging):
    df=get_sheet("users",debugging)
    if debugging:
        st.write(f"Trying to match subId={subId}")  
        st.dataframe(df)
    for index, row in df.iterrows():
        if debugging:
            st.write(f"Row={row}")
        if row['sub']==subId:
            row_dict=row.to_dict()
            if debugging:
                st.write(f"Found row-dict={row_dict}")
            return row_dict
    return None

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

def show_sheets(debugging=False):
    st.write("Sheets:")
    for sheet in sheets:
        df=get_sheet(sheet,debugging)
        st.write(f"## {sheet}")
        st.dataframe(df)

