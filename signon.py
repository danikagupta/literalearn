import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import urllib.parse
import pandas as pd
import requests

import cookiestore
import datastore
   

# Replace these with your client details
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_uri = st.secrets["redirect_url"]  # This must match the redirect URI in your OAuth provider settings
# redirect_url= "https://orange-happiness-v5vqwj5qp7q2p996-8501.app.github.dev/"
scope='email profile'
authorization_endpoint = 'https://accounts.google.com/o/oauth2/auth'
token_endpoint = 'https://oauth2.googleapis.com/token'
userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
st.sidebar.markdown(f"Secrets:\n {st.secrets}")
st.sidebar.markdown(f"State:\n {st.session_state}")
st.sidebar.markdown(f"Params:\n {st.experimental_get_query_params()}")



def exchange_code_for_token(code):
    token_url = 'https://oauth2.googleapis.com/token'
    # Prepare the data for the token request
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    # Make a POST request to the token endpoint
    response = requests.post(token_url, data=data)
    response_data = response.json()
    # Handle possible errors
    if response.status_code != 200:
        raise Exception("Failed to retrieve token: " + response_data.get('error_description', ''))
    return response_data['access_token']

def get_user_info(access_token):
    user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(user_info_url, headers=headers)
    user_info = response.json()
    # Handle possible errors
    if response.status_code != 200:
        raise Exception("Failed to retrieve user info: " + user_info.get('error_description', ''))
    return user_info


def process_user_info(user_info,debugging):
    df=datastore.get_sheet("users")
    subId="google-"+str(user_info['sub'])
    if debugging:
        st.sidebar.write(f"Trying to match subId={subId}")  
        st.sidebar.dataframe(df)
    df=df[df['sub']==subId]
    if debugging:
        st.sidebar.write(f"After match subId={subId}")  
        st.sidebar.dataframe(df)
    if(len(df)>0):
        if debugging:
            st.sidebar.write("You are in the list")
    else:
        if debugging:
            st.sidebar.write("You are not in the list. Adding you.")
        #datastore.add_to_sheet("users",[subId,user_info['name'],'hi','en',3,2],debugging)
        datastore.add_to_sheet("users",[subId,user_info['name']],debugging)

def main(debugging=False):
    if debugging:
        st.title('OAuth with Streamlit SIGNON-PY')

    aaa=""" 
    usercookie_name=cookiestore.cookie_manager.get(cookie=cookiestore.usercookie_name)
    usercookie_id=cookiestore.cookie_manager.get(cookie=cookiestore.usercookie_id)
    if usercookie_id is None:
        if debugging:
            st.write("No user found")
    else:
        if debugging:
            st.write(f"User found: {usercookie_id}")
        print(f"Calling process_user_info because UserCookie is set {usercookie_id} with {usercookie_name}.")
        process_user_info({'sub':usercookie_id,'name':usercookie_name},debugging)
        return
    """

    # Initialize the session
    session = OAuth2Session(client_id, client_secret, scope=scope, redirect_uri=redirect_uri)

    # Check if the user is logged in
    if 'user_info' in st.session_state:
        user_info = st.session_state['user_info']
        if debugging:
            st.write(f"1. Welcome {user_info['name']}!")
        #cookiestore.cookie_manager.set(cookiestore.usercookie_name,user_info['name'])
        cookiestore.cookie_manager.set(cookiestore.usercookie_id,user_info['sub'])
        print(f"Calling process_user_info because user info is in session state with {user_info}.")
        process_user_info(user_info,debugging)
        #XXX
        # Do the main thing here
    elif 'scope' in st.experimental_get_query_params():
        # Exchange the code for a token
        try:
            token = exchange_code_for_token(st.experimental_get_query_params()['code'])
            user_info = get_user_info(token)
            st.session_state['token'] = token
            st.session_state['user_info'] = user_info
            st.session_state['states_seen'] = "Passed 2"
            cookiestore.cookie_manager.set(cookiestore.usercookie_id,user_info['sub'])
            print("Success in exchange_code_for_token.")
            if debugging:
                st.write("2. Welcome, ", user_info['name'])
            st.rerun()
        except:
            print("Remove query parameters in exchange_code_for_token.")
            cookiestore.remove_query_params()
    else:
        # Generate the authorization URL and state, save the state
        uri, state = session.create_authorization_url(authorization_endpoint)
        st.session_state['state'] = state

        # Display the login link
        #st.markdown(f'[Login with Google]({uri})')
        cookiestore.same_window(uri,"Login with Google")  

        # Handle the callback from the OAuth provider
        params = st.experimental_get_query_params()
        if 'code' in params and params.get('state') == st.session_state.get('state'):
            # Exchange the code for a token
            token = session.fetch_token(token_endpoint, authorization_response=st.experimental_get_url())
            st.session_state['token'] = token
            st.experimental_rerun()

if __name__ == '__main__':
    main()