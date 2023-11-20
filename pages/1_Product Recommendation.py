from openai_na import get_assistant_response, text_to_speech
from PIL import Image
import streamlit as st
from audiorecorder import audiorecorder
import os
from openai import OpenAI

# Set the title
st.title('Product Recommendation Assistant')

             
# Set OpenAI API key and initialize client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message
with st.chat_message("assistant"):
    st.write("Hello, how can I help you today?")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept text user input
user_input = st.chat_input("Texted the Assistant")

# Check for new input (audio or text) and process it
new_input = user_input or prompt
if new_input:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": new_input})
    with st.chat_message("user"):
        st.markdown(new_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response, is_concluded, markdown = get_assistant_response(new_input)
            st.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Generating speech (if needed)
            with st.spinner("Generating speech..."):
                text_to_speech(full_response)
                st.audio("output.mp3", format="audio/mp3")

    if is_concluded:
        with st.spinner("Generating email..."):
            st.markdown(markdown, unsafe_allow_html=True)
            image = Image.open('image.jpg')
            st.image(image, width=300)
