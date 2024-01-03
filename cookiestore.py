import streamlit as st
import extra_streamlit_components as stx

st.write("# Cookie Manager")

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
usercookie_name='LiteraLearnUser'

def same_window(uri,msg):
    st.markdown(f"""
            <a href="{uri}" target = "_self">  {msg} </a>
        """, unsafe_allow_html=True)

def cookie_ui():

    st.subheader("All Cookies:")
    cookies = cookie_manager.get_all()
    st.write(cookies)

    c4, c1, c2, c3 = st.columns(4)

    with c1:
        st.subheader("Get Cookie:")
        cookie = st.text_input("Cookie", key="0")
        clicked = st.button("Get")
        if clicked:
            value = cookie_manager.get(cookie=cookie)
            st.write(value)
    with c2:
        st.subheader("Set Cookie:")
        cookie = st.text_input("Cookie", key="1")
        val = st.text_input("Value")
        if st.button("Add"):
            cookie_manager.set(cookie, val) # Expires in a day by default
    with c3:
        st.subheader("Delete Cookie:")
        cookie = st.text_input("Cookie", key="2")
        if st.button("Delete"):
            cookie_manager.delete(cookie)
    with c4:
        st.subheader("Delete LOGIN Cookie")
        if st.button("Delete LOGIN"):
            cookie_manager.delete(usercookie_name)

    