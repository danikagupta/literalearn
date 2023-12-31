import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
from openai import OpenAI
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
import pandas as pd
from google.cloud import speech
from google.oauth2 import service_account


def transcribe_audio_whisper(file_path,language_iso):
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

def transcribe_audio(file_path,language_iso):
    gcs_credentials = st.secrets["connections"]["gcs"]
    credentials = service_account.Credentials.from_service_account_info(gcs_credentials)
    client = speech.SpeechClient(credentials=credentials)
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    # Configure the request with the language and audio file
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        #encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_iso,
        audio_channel_count=2,
    )
    # Send the request to Google's Speech-to-Text API
    google_response = client.recognize(config=config, audio=audio)
    response=""
    for result in google_response.results:
        response+=result.alternatives[0].transcript

    print(f"Response: {google_response}")
    print(f"Response.results: {google_response.results}")
    st.sidebar.markdown(f"Response: {google_response}")
    # Print the transcription of the first alternative of the first result
    for result in google_response.results:
        print(f"Result: {result}")
        print(f"Result.alternatives: {result.alternatives}")
        print(f"Result.alternatives[0]: {result.alternatives[0]}")
        print("Transcription: {}".format(result.alternatives[0].transcript))
    return response


def bleu(hypothesis, reference):
  # Tokenize the hypothesis and reference strings.
  hypothesis_tokens = word_tokenize(hypothesis)
  reference_tokens = word_tokenize(reference)
  print(f"Reference tokens: {reference_tokens}, hypothesis tokens: {hypothesis_tokens}, reference: {reference}, hypothesis: {hypothesis}")
  st.markdown(f"Reference tokens: {reference_tokens}, hypothesis tokens: {hypothesis_tokens}, reference: {reference}, hypothesis: {hypothesis}")
  # Calculate the BLEU score.
  smoothie=SmoothingFunction().method1
  bleu_score = sentence_bleu([reference_tokens], hypothesis_tokens,smoothing_function=smoothie)
  return bleu_score

@st.cache_data
def getCSV():
    return pd.read_csv("assets/sentences.csv")

def getSentence(language,difficulty):
    df=getCSV()
    with st.sidebar.expander("Show more"):
      st.dataframe(df)
      df=df[df["language"]==language]
      df=df[df["difficulty"]==difficulty]
      sentence=df.sample().iloc[0]["sentence"]
      st.markdown(f"## Sentence={sentence}")
    return sentence
    
#
# Main code
#
# st.sidebar.write(f"Secrets={st.secrets}")
st.sidebar.write(st.secrets.keys())
#
languages={"हिंदी":"hi","English":"en","മലയാളം":"ml","සිංහල":"si"}
main_instruction={"hi":"साफ़ से बोलें","en":"Speak clearly","ml":"വ്യക്തമായി സംസാരിക്കുക","si":"පැහැදිලිව කතා කරන්න"}

nltk_data_path = os.path.join(os.getcwd(),"nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

st.sidebar.title("LiteraLearn")
st.sidebar.image("assets/icon128px-red.png")
language_select=st.sidebar.selectbox("Language",options=languages.keys())
language_iso=languages[language_select]
instruction=main_instruction[language_iso]
sentence=getSentence(language_iso,1)
st.markdown(f"## {instruction}")
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
    sc=bleu(transcription,sentence)
    st.markdown(f"BLEU score: {sc}")
 