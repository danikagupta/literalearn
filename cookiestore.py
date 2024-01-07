import streamlit as st
import extra_streamlit_components as stx
import base64
import os

# st.write("# Cookie Manager")

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
usercookie_id='LiteraLearnUserId'
usercookie_name='LiteraLearnUserName'
usercookie_email='LiteraLearnUserEmail'

def get_audio_html_code(audiofile):
    audio_html_code="""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    /* Style the button */
    .help-button {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        text-align: center;
    }

    /* Style for the Help Icon, you can replace it with an actual image or icon */
    .help-icon {
        padding-right: 5px;
    }
</style>
</head>
<body>

<!-- Button with a help icon -->
<button class="help-button" onclick="playAudio()">
    <span class="help-icon">?</span>
    Help
</button>
""" + f"""
<!-- Audio element -->
<audio id="myAudio">
  <source src="{audiofile}" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
""" + """
<script>
// Function to play the audio
function playAudio() {
  var audio = document.getElementById("myAudio");
  audio.play();
}
</script>

</body>
</html>
"""
    return audio_html_code

def same_window(uri,msg):
    st.markdown(f"""
            <a href="{uri}" target = "_self">  {msg} </a>
        """, unsafe_allow_html=True)

def not_same_window(uri,image_path,msg):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    markdown = f'<a href="{uri}" target="_blank"><img src="data:image/png;base64,{encoded_string}" alt={msg}></a>'

    # Display the clickable image
    st.markdown(markdown, unsafe_allow_html=True)
    
def not_same_window_original(uri,msg):
    st.markdown(f"""
            <a href="{uri}" target = "_blank">  {msg} </a>
        """, unsafe_allow_html=True)

def remove_query_params():
    current_params = st.experimental_get_query_params()
    params=list(current_params.keys())
    for param in params:
        del current_params[param]
    st.experimental_set_query_params(**current_params)

def get_music_code(audiofile):
    fname=os.path.join(os.getcwd(),"audiofiles",audiofile)
    ht=get_audio_html_code(fname)
    return ht



def cookie_ui():

    st.subheader("All Cookies:")
    cookies = cookie_manager.get_all()
    st.write(cookies)

    c4, c1, c2, c3, c5 = st.columns(5)

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
    with c5:
        st.subheader("Delete ALL Cookies")
        if st.button("Delete ALL Cookies"):
            for cookie in cookies.keys():
                cookie_manager.delete(cookie)

    