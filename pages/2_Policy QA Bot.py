import streamlit as st
from openai_qa import get_assistant_response
from audiorecorder import audiorecorder
import os
from openai import OpenAI
from openai_qa import *

# Set your OpenAI API key from an environment variable
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Display the title
st.title('Policy QA Bot Assistant')

# Initialize 'prompt' variable
prompt = ""

# Audio recorder
audio = audiorecorder("Speak to the Assistant", "Click Again When Done")

# Process audio input if any
if len(audio) > 0:
    audio.export("audio.wav", format="wav")
    audio_file = open("audio.wav", "rb")
    prompt = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

# Initialize chat history if not already present
if "messages_qa" not in st.session_state:
    st.session_state.messages_qa = []

# Display welcome message
with st.chat_message("assistant"):
    st.write("Hello, how can I help you today?")

# Display previous chat messages
for message in st.session_state.messages_qa:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept text input from user
user_input = st.chat_input("Texted the Assistant")

# Check if there is new input and process it
new_input = user_input or prompt
if new_input:
    # Add user message to chat history and display it
    st.session_state.messages_qa.append({"role": "user", "content": new_input})
    with st.chat_message("user"):
        st.markdown(new_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = get_assistant_response(new_input)
            st.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages_qa.append({"role": "assistant", "content": full_response})

            # Generating speech (if needed)
            with st.spinner("Generating speech..."):
                text_to_speech(full_response)
                st.audio("output.mp3", format="audio/mp3")
