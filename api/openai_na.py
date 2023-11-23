import os
from openai import OpenAI
import time
import re
import requests

# Connect to Open AI   
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# Connect to the Assistant 
assistant_id = os.getenv("OPENAI_ASSISTANT_ID_NA")
assistant = client.beta.assistants.retrieve(assistant_id)

# Create thread for this user and run
thread = client.beta.threads.create()

def get_assistant_response(user_prompt):

    is_concluded = False
    markdown=""

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


    # check if the assistant has concluded the conversation - trigger 'Thank you for trusting your future with us. Have a wonderful day!'
    if "Have a wonderful day!" in output_text:
        is_concluded = True


    if is_concluded:
        # get all chat history, set the right order
        conversation_history = parse_message(results)
        conversation_history = conversation_history.replace('user','Value Customer')
        emails = parse_emails(conversation_history)

        # create sale pitch from chat history
        sales_pitch = client.chat.completions.create(
                        model="gpt-4-1106-preview",
                        messages=[
                            {"role": "system", "content": "You are a helpful respectful life insurance sales person."},
                            {"role": "user", "content": f"Write a creative two paragraph email sales pitch for the conversation history, that is..  {conversation_history} "}
                        ],
                        temperature=0,
                    )
        # generate the image, base on the subject line
        image = client.images.generate(
                        model="dall-e-3",
                        prompt=str(sales_pitch.choices[0].message.content.split('\n\n')[0]),
                        size="1024x1024",
                        quality="standard",
                        n=1,
                        )

        image_url = image.data[0].url
        # Download the image
        img_data = requests.get(image_url).content

        # Write the image data to a file
        with open(f'output/image.jpg', 'wb') as handler:
            handler.write(img_data)

        # email markdown
        markdown = f'<h2>Sample Email</h2>{sales_pitch.choices[0].message.content}'
      
    
    return output_text,is_concluded,markdown

def text_to_speech(text_input="The quick brown fox jumped over the lazy dog."):
    response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text_input
                )
    response.stream_to_file("output/output.mp3")

def parse_message(results):

    messages_history = [
                        (thread_message.created_at, thread_message.role, thread_message.content[0].text.value)
                        for thread_message in results.data
                        if thread_message.content[0].type == "text"
                        ]

    messages_history_ordered = sorted(messages_history, key=lambda x: x[0], reverse=False)

    # construct conversation history in chronological order
    conversation_history = "\n"
    for _, speaker, message in messages_history_ordered:
        conversation_history += f"{speaker} : {message}\n\n"

    return conversation_history


def parse_emails(conversation_history):
    emails=[]
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = list(set(re.findall(email_pattern, conversation_history)))
    return emails

