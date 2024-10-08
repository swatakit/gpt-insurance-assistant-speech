import streamlit as st
from audiorecorder import audiorecorder
import os
from openai import OpenAI
from api.openai_qa import *

# Set your OpenAI API key from an environment variable
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

def stick_header():

    # make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    background-color: white;
                    z-index: 999;
                }
                .fixed-header {
                    /* border-bottom: 1px solid black; */
                }
            </style>
        """,
        unsafe_allow_html=True
    )

# Initialize 'prompt' variable
prompt = ""

with st.container():
    stick_header()

    # Display the title
    st.title('Question and Answer Insurance Assistant')

    # set explanation 
    with st.expander("Assistants Role"):
        st.markdown("""
        This assistant provides answers to questions about **Etiqa Singapore's Insurance products**.
    """)

    # Audio recorder
    audio = audiorecorder("Speak to the Assistant", "Click Again When Done")

    # Process audio input if any
    if len(audio) > 0:
        audio.export("output/audio.wav", format="wav")
        audio_file = open("output/audio.wav", "rb")
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

# Accept text user input
user_input = st.chat_input("Chat with Assistant")

# Check for new input (audio or text) and process it
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
            st.audio("output/output.mp3", format="audio/mp3")
