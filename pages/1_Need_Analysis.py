import streamlit as st
from openai_na import *
from PIL import Image
from audiorecorder import audiorecorder


# Connect to Open AI   
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

st.title('Chat with Insurance Needs & Product Recommendation Assistant')

# Initialize 'transcript' variable
transcript = ""

# Audio recorder
audio = audiorecorder("Speak to the Assistant", "Click Again When Done",key=1)

# Process audio input if any
if len(audio) > 0:
    audio.export("audio.wav", format="wav")
    audio_file = open("audio.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

# Initialize chat history  
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message
with st.chat_message("assistant"):
    st.write("Hello, how can I help you today? ")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("Message to the assistant")
user_input = prompt or transcript

if user_input:

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message_placeholder = st.empty()
            full_response,is_concluded,markdown = get_assistant_response(user_input)
            message_placeholder.markdown(full_response)

    with st.spinner("Generating speech..."):
        if message_placeholder != st.empty():
            text_to_speech(full_response)
            st.audio("output.mp3", format="audio/mp3")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    if is_concluded:
        with st.spinner("Generating email..."):
            st.markdown(markdown,unsafe_allow_html = True)
            image = Image.open('image.jpg')
            st.image(image,width =300)

