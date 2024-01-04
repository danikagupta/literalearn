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

def get_user_status(subId,debugging):
    df=get_sheet("status",debugging)
    print(f"get-user-status initially found {df} OR {df.to_dict()}")
    if debugging:
        st.write(f"Trying to match subId={subId}")  
        st.dataframe(df)
    df=df[df['sub']==subId]
    print(f"get-user-status found {df} returning {df.to_dict()}")
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

def update_user_lang(subId,lang,debugging):
    print(f"Update user lang INPUT {subId} {lang} {debugging}}}")
    row_dict=get_user_row(subId,debugging)
    params = {"tabId": "Sheet1"}
    row_dict['language']=lang
    url=sheet_mapping["users"]
    print(f"Update user lang Request {row_dict} URL {url}}}")
    r = requests.put(url = url, params = params, json = row_dict)
    result = r.json()
    # if debugging:
    print(f"Update user lang returns {result}")
    return result
  

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


def add_user_level(subId,name,lang,level,debugging):
    print(f"Add user level INPUT {subId}:{name}:{lang}:{level}:{debugging}}}")

    row=[subId,name,lang,level,0,"NA"]
    result=add_to_sheet("status",row,True)
    return result 