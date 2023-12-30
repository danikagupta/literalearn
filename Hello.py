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
import whisper

def transcribe_audio(file_path):
    # Load the pre-trained Whisper model
    model = whisper.load_model("base")  # You can choose other models like "small", "medium", "large"

    # Load the audio file
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    # (Optional) Print the detected language
    # Mel spectrogram generation (optional to show the language detection)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # Transcribe the audio
    options = whisper.DecodingOptions()
    result = model.transcribe(mel, options)

    # Return the transcription
    return result["text"]

#
# Main code
#

path_myrecording = os.path.join(os.getcwd(),"audiofiles","myrecording.wav")
audio_bytes = audio_recorder(text="")
if audio_bytes:
    st.markdown("Just saw fresh audio bytes!")
    st.audio(audio_bytes, format="audio/wav")
    with open(path_myrecording, mode='bw') as f:
        f.write(audio_bytes)
        f.close()
    transcription = transcribe_audio(path_myrecording)
    st.markdown("Transcription:", transcription)

aaa="""


audio_bytes = audio_recorder(
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="6x",
)



from st_audiorec import st_audiorec

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav') 
st.write("# Welcome to Streamlit! 👋")
"""
