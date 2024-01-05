import streamlit as st
from openai import OpenAI

from google.cloud import speech
from google.oauth2 import service_account

from audio_recorder_streamlit import audio_recorder

import os
import json

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

def function_print_similarity_score(str1: str, str2: str) -> str:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    functions = [{
        "name": "print_similarity_score",
        "description": "A function that prints the similarity score of two strings",
        "parameters": {
            "type": "object",
            "properties": {
                "similarity_score": {
                    "type": "integer",
                    "description": "The similarity score."
                },
            }, "required": ["similarity_score"],
        }
    }]
    llm_input=f"""
    You are a language reviewer responsible for reviewing the similarity of two sentences.
    The user is being given a sentence, and asked to repeat the sentence themselves.
    As such, the scoring has to be very strict.
    Please note that the specifc words and word-order are important, not just the meaning.
    On a scale of 1-100, with 100 being the most similar, how similar are these: "{str1}", and "{str2}".
    """
    messages = [{"role": "user", "content": llm_input}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, functions=functions, function_call={"name": "print_similarity_score"})
    #print(f"Response is: {response}")
    function_call = response. choices [0].message.function_call
    #print(f"Function call is: {function_call}")
    argument = json.loads(function_call.arguments)
    #print(f"Response function parameters are: {argument}")
    print(f"For inputs {str1} and {str2}, the similarity score is: {argument}")
    return argument



def ask_question(user_sub,selected_question,language,debugging):
    st.markdown(f"## Ask Question: {selected_question} for user {user_sub}") 
    main_instruction={"hi":"साफ़ से बोलें","en":"Speak clearly","ml":"വ്യക്തമായി സംസാരിക്കുക","si":"පැහැදිලිව කතා කරන්න"}  
    language_iso=language
    instruction=main_instruction[language_iso]
    sentence=selected_question
    st.markdown(f"## {instruction}")
    col1,col2=st.columns(2)
    col1.markdown(f"{sentence}")
    # No audio at this time; will investigate TTS. 
    # col2.audio(audiobytes, format="audio/wav")

    path_myrecording = os.path.join(os.getcwd(),"audiofiles","myrecording.wav")
    audio_bytes = audio_recorder(text="")
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with open(path_myrecording, mode='bw') as f:
            f.write(audio_bytes)
            f.close()
        transcription = transcribe_audio(path_myrecording,language_iso)
        st.markdown(f"Transcription: {transcription}")
        sc2=function_print_similarity_score(transcription,sentence)
        st.markdown(f"OpenAI score: {sc2}") 