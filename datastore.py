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

def get_questions(lang,level,debugging):
    df=get_sheet("sentences",debugging)
    df['level'] = pd.to_numeric(df['level'])
    if debugging:
        st.write(f"Trying to match lang={lang} and level={level}")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    df=df[df['language']==lang]
    if debugging:
        st.write(f"After filter for lang={lang}  ")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    df=df[df['level']==level]
    if debugging:
        st.write(f"After filter for  level={level}")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    if debugging:
        st.write(f"Found {df} returning {df.to_dict()}")
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

def get_user_question_row(user_sub,language,question,debugging):
    df=get_sheet("status",debugging)
    if debugging:
        st.write(f"Trying to match subId={user_sub} and language={language} and question={question}")  
        st.dataframe(df)
    for index, row in df.iterrows():
        if debugging:
            st.write(f"Row={row}")
        if row['sub']==user_sub and row['question']==question and row['language']==language:
            row_dict=row.to_dict()
            if debugging:
                st.write(f"Found row-dict={row_dict}")
            return row_dict
    return None

def get_user_question_answers(user_sub,language,level,debugging):
    df=get_sheet("status",debugging)
    df['level'] = pd.to_numeric(df['level'])
    if debugging:
        st.write(f"Trying to match subId={user_sub} and language={language} and level={level}")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    df=df[df['sub']==user_sub]
    if debugging:
        st.write(f"After filter for sub={user_sub}  ")  
        st.dataframe(df)
    df=df[df['language']==language]
    if debugging:
        st.write(f"After filter for lang={language}  ")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    df=df[df['level']==level]
    if debugging:
        st.write(f"After filter for  level={level}")  
        st.dataframe(df)
        st.write(f"Data types are {df.dtypes}")
    if debugging:
        st.write(f"Found {df} returning {df.to_dict()}")
    return df

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

def add_rows_to_sheet(sheet,rows,debugging=False):
    if debugging:
        print(f"DataStore.AddRowsToSheet: Adding {rows} to {sheet}") 
    url=sheet_mapping[sheet]
    params = {"tabId": "Sheet1"}
    r = requests.post(url = url, params = params, json = rows)
    result = r.json()
    if debugging:
        print(result)   
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
    #result=add_to_sheet("status",row,True)
    questions=get_questions(lang,level,debugging)
    result=add_questions_for_user(subId,name,questions,debugging)
    return result 


def add_questions_for_user(subId,name,questions,debugging):
    print(f"Add questions for user: INPUT {subId} {questions} {debugging}")
    rows=[]
    for index, question in questions.iterrows():
        row=[subId,name,question['language'],question['level'],question['sentence'],'No']
        rows.append(row)
    print(f"Add questions for user: ADDING {rows}")
    result=add_rows_to_sheet("status",rows,debugging)
    return result

def update_answer(user_sub,language,question,debugging):
    # st.markdown(f"# Unfinished business: update_answer {user_sub} {language} {question} {debugging}")
    # print(f"Update user lang INPUT {subId} {lang} {debugging}}}")
    row_dict=get_user_question_row(user_sub,language,question,debugging)
    params = {"tabId": "Sheet1"}
    row_dict['answered']="Yes"
    url=sheet_mapping["status"]
    print(f"Update user lang Request {row_dict} URL {url}}}")
    r = requests.put(url = url, params = params, json = row_dict)
    result = r.json()
    # if debugging:
    print(f"Update user answer returns {result}")
    return result

def get_success_rate(user_sub,language,level,last_question,debugging):
    if debugging:
        st.markdown(f"#  get_success_rate {user_sub} {language} {level} {debugging}")
    df=get_user_question_answers(user_sub,language,level,debugging)
    if debugging:
        st.markdown("Returned DF for Get-Success-Rate")
        st.dataframe(df)
    df.loc[df['question'] == last_question, 'answered'] = 'Yes'
    yes_count = (df['answered'] == 'Yes').sum()
    yes_pct=(yes_count/len(df))*100
    if debugging:
        st.markdown(f"Returned DF for Get-Success-Rate - post-update {yes_count} {yes_pct}")
        st.dataframe(df)
    return yes_pct

def enable_english(user_sub,user_name,debugging):
    print(f"Enable English INPUT {user_sub} {user_name} {debugging}}}")
    df=get_user_status(user_sub,debugging)
    df=df[df['language']=='English']
    if(len(df)>0):
        print(f"Enable English: Already enabled")
        return -1
    else:
        result=add_user_level(user_sub,user_name,'en',5,debugging)
    return result