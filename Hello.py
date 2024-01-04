import streamlit as st
import cookiestore
import signon

def send_to_customer_service(debugging):
    print("We're sorry, but we can't identify customer.")
    if debugging:
        st.markdown("## We're sorry, but we can't identify you.")

def send_to_language_selection(user_sub,user_name,debugging):
    st.markdown(f"## Menu for language selection for {user_sub,user_name,debugging}.")

def run_once(debugging):
    if debugging:
        st.write("# Hello world!! (from main Hello.py)")
    # cookiestore.cookie_ui()
    signon.main(debugging)
    #
    # Case 1: No user (e.g. Invalid Google Login). Provide a helpful message for them to reach Customer Service.
    # Case 2: Initial user (needs language selection). Provide a menu with langauge choices. Save back in Persistent Storage.
    # Case 3: Existing user - only native language. No English access yet. Ask questions in native language. Qualify for English access.
    # Case 4: Existing user - native language and English access. Ask questions interleaved between native and Engligh. Promote along.
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
    user_record=signon.datastore.get_user_row(user_sub,debugging)
    if user_record is None:
        if(debugging):
            st.write(f"User record is None. {user_info}")
        send_to_customer_service()
        return
    user_name=user_record['name']
    st.markdown(f"## Welcome {user_name}!")
    if debugging:
        print(f"For user {user_name}, got user record {user_record}")
    if 'lang' not in user_record:
        send_to_language_selection(user_sub,user_name,debugging)
        return
    st.markdown(f"## Unfinished business for {user_name}!")

def main():
    run_once(False)


main()