# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
from openai import OpenAI


def transcribe_audio(file_path,language_iso):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        language=language_iso,
        response_format="text"
    )
 
    print(f"Transcript: {transcript}")
    return transcript

#
# Main code
#
languages={"Hindi":"hi","English":"en","Malayalam":"ml"}
sentences={"Hindi":"आप कैसे हैं?","English":"How are you?","Malayalam":"നിങ്ങൾ എങ്ങനെ ഉണ്ട്?"}


language_select=st.selectbox("Select language",options=languages.keys())
language_iso=languages[language_select]
sentence=sentences[language_select]
st.markdown(f"# Speak slowly and clearly (needs translation)")
st.markdown(f"{sentence}")

path_myrecording = os.path.join(os.getcwd(),"audiofiles","myrecording.wav")
audio_bytes = audio_recorder(text="")
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with open(path_myrecording, mode='bw') as f:
        f.write(audio_bytes)
        f.close()
    transcription = transcribe_audio(path_myrecording,language_iso)
    st.markdown(f"Transcription: {transcription}")
 