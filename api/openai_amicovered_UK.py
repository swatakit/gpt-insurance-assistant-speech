import os
from openai import OpenAI
import time
import re
import requests

# Connect to Open AI   
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Connect to the Assistant 
assistant_id = os.environ["OPENAI_ASSISTANT_ID_UK"]
assistant = client.beta.assistants.retrieve(assistant_id)

# Create thread for this user and run
thread = client.beta.threads.create()

def get_assistant_response(user_prompt):
    # Create a message from user prompt
    thread_message = client.beta.threads.messages.create(
                        thread.id,
                        role="user",
                        content=user_prompt
                        )
    
    # Run the assistant
    run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
            )
    
    # Display assistant's response
    run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
                )
    
    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
                )


    results = client.beta.threads.messages.list(
                thread_id=thread.id
                )
    
    first_id = results.first_id
    responses = []

    for thread_message in results.data:

        # Check if the message is from the assistant, and it is the first message on the top of the stack, which is the lastest response
        if thread_message.role == 'assistant' and thread_message.id == first_id:  

            # Assuming there's only one MessageContentText object in the content list
            assistant_response = thread_message.content[0].text.value
            responses.append(assistant_response)

    # Now `responses` contains all messages from the assistant
    output_text = " ".join(responses)

    return output_text

def text_to_speech(text_input="The quick brown fox jumped over the lazy dog."):
    response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text_input
                )
    response.stream_to_file("output/output.mp3")