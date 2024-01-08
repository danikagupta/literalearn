import streamlit as st
import cookiestore
import signon
import datastore
import quizworld

import random
import pandas as pd
import math

st.set_page_config(
    page_title="LiteraLearn",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

MAX_LEVEL=11
PASSING_SCORE_VERBAL=60
PASSING_SCORE_LANG=70
SCORE_ENGLISH_ENABLE=60

GIF_URL="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGxldmIxMXZsbTkxbHR3ejg1MzgwM3pwNDMwYzAzZGIxcGY5bGZ3ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OC0aNQsPvqiEhFDQ9p/giphy.gif"

languages={"English":"en","हिंदी":"hi","മലയാളം":"ml","සිංහල":"si"}
level_select={"hi":"साफ़ से बोलें (level)","en":"What's your level?","ml":"വ്യക്തമായി സംസാരിക്കുക (level)","si":"පැහැදිලිව කතා කරන්න (level)"}
levels=[1,2,3,4,5,6,7,8,9,10,11,12]

def setup_sidebar_start():
    st.sidebar.markdown("# LiteraLearn")
    st.sidebar.image("assets/icon128px-red.png")

def setup_sidebar_end():
    images=["assets/img1.jpg","assets/img2.jpg","assets/img3.jpg",
            "assets/img4.jpg","assets/img5.jpg","assets/img6.jpg",
            "assets/img7.jpg","assets/img8.jpg","assets/img9.jpg",
            "assets/img10.jpg","assets/img11.jpg","assets/img12.jpg",
            "assets/img13.jpg"]
    random_image=random.choice(images)
    st.sidebar.image(random_image)
    bu=st.sidebar.button("Reset", type="primary")
    if bu:
        st.rerun()

def send_to_customer_service(debugging):
    print("We're sorry, but we can't identify customer.")
    if debugging:
        st.markdown("## We're sorry, but we can't identify you.")

def send_to_language_selection(user_sub,user_name,debugging):
    st.markdown(f"## Please choose your language.")
    language_select=st.selectbox(" ",options=languages.keys(), index=None)
    if language_select:
        language_iso=languages[language_select]
        st.session_state['user_info']['lang']=language_iso
        datastore.update_user_lang(user_sub,language_iso,debugging)

def send_to_level_selection(user_sub,user_name,user_native_language,debugging):
    print("Starting level selection")
    st.markdown(f"## {level_select[user_native_language]}.")
    level_selected=st.selectbox(" ",options=levels, index=None)
    if level_selected:
        st.markdown(f"## {user_native_language} {level_selected}.")
        print(f"## {user_native_language} {level_selected}.")
        datastore.add_user_level(user_sub,user_name,user_native_language,level_selected,debugging)

def process_question(user_sub,user_name,level,question,audiofile,language,languages,debugging):
    score=quizworld.ask_question(user_sub,user_name,question,audiofile,language,level,languages,debugging)
    if score>=PASSING_SCORE_VERBAL:
        st.write(datastore.get_i18n('correctAnswer',language,debugging))
        if debugging:
            st.markdown(f"## Congratulations! You answered correctly.")
        st.image(GIF_URL,width=200)
        datastore.update_answer(user_sub,language,question,debugging)
        del st.session_state['selected_question']
        level_score=datastore.get_success_rate(user_sub,language,level,question,debugging)
        print(f"Checking language. Level score is {level_score} and level is {level} and passing score is {PASSING_SCORE_LANG}")
        if level_score>PASSING_SCORE_LANG:
            st.markdown(f"🎉 🎉 🎉  {datastore.get_i18n('levelUp',language,debugging)} 🎉 🎉 🎉 ")    
            st.balloons()
            if(level<MAX_LEVEL):
                datastore.add_user_level(user_sub,user_name,language,level+1,debugging)
        if level_score>SCORE_ENGLISH_ENABLE:
            #st.markdown("Congratulations! You have passed the English Enablement level. You will now be able to answer questions in English.")
            st.snow()
            datastore.enable_english(user_sub,user_name,debugging)
    else:
        st.write(datastore.get_i18n('wrongAnswer',language,debugging))
        if debugging:
            st.markdown(f"## Sorry, but you answered incorrectly.")
            st.markdown(f"# {score} < {PASSING_SCORE_VERBAL}")
    bu=st.button("Next Question")
    if bu:
        # TO-DO. Delete other state elements, including the transcript.
        if 'selected_question' in st.session_state:
            del st.session_state['selected_question']
        print("Rerunning due to Next Question")
        st.rerun()
    

def run_once(debugging):
    if debugging:
        st.write("# Hello world!! (from main Hello.py)")
    # cookiestore.cookie_ui()
    signon.main(languages,debugging)
    #
    # Case 1: No user (e.g. Invalid Google Login). Provide a helpful message for them to reach Customer Service.
    # Case 2: Initial user (needs language selection). Provide a menu with langauge choices. Save back in Persistent Storage.
    # Case 3: User selected language. Now needs to select level.
    # Case 4: Existing user - only native language. No English access yet. Ask questions in native language. Qualify for English access.
    # Case 5: Existing user - native language and English access. Ask questions interleaved between native and Engligh. Promote along.
    #
    if (debugging):
        print(f"Got session state info {st.session_state}")
    if 'user_info' not in st.session_state:
        if(debugging):
            st.write(f"st session state doen't have user info. {st.session_state}")
        send_to_customer_service(debugging)
        return
    user_info=st.session_state['user_info']
    print(f"Got user info {user_info}")
    if 'sub' not in user_info:
        if(debugging):
            st.write(f"user info doesn't have sub. {user_info}")
        send_to_customer_service(debugging)
        return
    user_sub="google-"+user_info['sub']
    print(f"Got sub {user_sub}")
    user_df=datastore.get_user_row(user_sub,debugging)
    if user_df is None:
        if(debugging):
            st.write(f"User DF is None. {user_info}")
        send_to_customer_service(debugging)
        return
    user_record=user_df.to_dict()
    if user_record is None:
        if(debugging):
            st.write(f"User record is None. {user_info}")
        send_to_customer_service(debugging)
        return
    user_name=user_record['name']
    if debugging:
        st.markdown(f"## Welcome {user_name}!")
    if 'selected_question' in st.session_state:
        # User is answering a question in progress; we can skip other steps.
        selected_question=st.session_state['selected_question']
        audio_file=st.session_state['audio_file']
        user_sub=st.session_state['user_sub']
        user_name=st.session_state['user_name']
        selected_language=st.session_state['selected_language']
        highest_level=st.session_state['highest_level']
        process_question(user_sub,user_name,highest_level,selected_question,audio_file,selected_language,languages,debugging) 
        return
    #if debugging:
    print(f"For user {user_name}, got user record {user_record}")
    if 'language' not in user_record:
        send_to_language_selection(user_sub,user_name,debugging)
        return
    user_native_language=user_record['language']
    if user_native_language in languages.values():
        if debugging:
            st.markdown(f"## Found {user_native_language} for {user_name}")   
    else:
        if debugging:
            st.markdown(f"## Found {user_native_language} for {user_name}") 
        print(f"Didnt find langauge for {user_record}")
        send_to_language_selection(user_sub,user_name,debugging)
        return
    
    df_user_lang=datastore.get_user_status(user_sub,debugging)

    if df_user_lang is None:
        st.markdown(f"## We're sorry, but there is a DF problem. Please contact customer support.")
        return
    user_languages=df_user_lang['language'].unique()
    print(f"User languages are {user_languages}")
    if len(user_languages)==0:
        send_to_level_selection(user_sub,user_name,user_native_language,debugging)  
        return
    #
    # Start showing user questions in corresponding languages and levels
    # 
    #
    if debugging:
        st.markdown(f"Final steps for {user_name} with {user_record} and languages {user_languages}!")
        st.dataframe(df_user_lang)
    filtered_df=df_user_lang.copy()
    # Step 1: Select records where answered is "No"
    filtered_df = filtered_df[filtered_df['answered'] == "No"]
    filtered_df['level'] = pd.to_numeric(filtered_df['level'])
    # Step 2: Randomly Select a Language
    available_languages=filtered_df['language'].unique()
    selected_language = random.choice(filtered_df['language'].unique())
    # Step 2: Filter Data for Selected Language
    filtered_df = filtered_df[filtered_df['language'] == selected_language]
    # Step 3: Find the Record with the Highest Level
    highest_level = filtered_df['level'].max()
    filtered_df = filtered_df[filtered_df['level'] == highest_level]
    if debugging:
        print(f"Higest level= {highest_level}")
        st.markdown(f"## HLR: {highest_level}")
        st.dataframe(filtered_df)
    selected_question = random.choice(filtered_df['question'].unique())
    audio_file=filtered_df[filtered_df['question']==selected_question]['audiofile'].iloc[0]
    st.session_state['selected_question']=selected_question
    st.session_state['user_sub']=user_sub
    st.session_state['user_name']=user_name
    st.session_state['selected_language']=selected_language
    st.session_state['highest_level']=highest_level
    st.session_state['audio_file']=audio_file
    process_question(user_sub,user_name,highest_level,selected_question,audio_file,selected_language,languages,debugging)

def main():
    setup_sidebar_start()
    # datastore.main()

    run_once(False)
    setup_sidebar_end()


main()