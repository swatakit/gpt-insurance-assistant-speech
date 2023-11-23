import streamlit as st
from PIL import Image

# st.title('Welcome to our AI insurance assistant, powered by ChatGPT')
# st.write("Our assistant is designed to provide you with quick and efficient responses to anything related to insurance. With the help of advanced AI models, our assistant can analyze vast amounts of data to provide personalized experiences based on your needs. Whether you’re looking to buy an insurance product or information about your policy or coverage, our assistant is here to help. Our goal is to make insurance simple, transparent, and accessible to everyone. So, go ahead and ask us anything, we’re always here to help! ")
# st.sidebar.markdown("Welcome")

image = Image.open('image/welcome.png')
st.image(image)

st.caption('Powered by :blue[OpenAI] APIs :sunglasses:')

st.write("We have created :blue[Two Unique Insurance Assistants ] which are designed to provide customers with clear and concise information regarding our: \
\n\n 1. Suite of Insurance Products \n\n 2. Assist Potential New Customers in determining which Life Insurance Product is best for them.")


st.title('Quick Win Insurance Use Cases')

st.write("The following provides a highlevel overview of Insurance User Cases that Generative AI as recently unlocked.  These user cases are generally considered quick wins.")

st.divider()

image = Image.open('image/genai_usecase.png')
st.image(image, width=1000)



st.divider()
st.title('Customer Benefits ')
st.subheader("Policy Information Question and Answers")

st.write(":blue[On Demand Customer Service:] \
         Customers can engage with the AI agent at there convenience. \
         \n\n :blue[Streamless Experience Across Chats:] The AI agents can tailor responses based on the content of the entire conversation with the customer. \
         \n\n :blue[Consistency in Responses:] The AI agent can provide consistent and accurate information, while operating within constraints.  \
         \n\n :blue[Educational and Empowering:] AI systems can be designed to provide customers with insights into why certain products are recommended. ")
  


st.divider()
st.subheader("Needs Assessment & Product Recommendation")

st.write(":blue[Personalized Recommendations:] Highly personalized insurance product recommendations that better match individual customer needs. \n\n :blue[Multilingual Support:] The AI agent have the capability to understand and respond in multiple languages, making it a versatile tool for global customer support. \n\n :blue[Speed and Efficiency:] AI systems can process information and generate recommendations much faster than traditional methods. ")
  

st.title('High Level System Architecture')

st.header("Assistants Architecture")

image = Image.open('image/agent_workflow.png')
st.image(image, width=1000)

st.divider()  

st.subheader("Product Recommendation Assistant")

st.write(":blue[Sample Instructions:] You are a highly skilled life insurance agent who provides life insurance product recommendations based on a customer's needs assessment. \
         You are polite with the customers and have a conversation with them to understand their insurance needs.Your objective: is to assist the \
         customer in deciding which life insurance policy they should purchase.....  \
         \n\n :blue[Constraints:] Never recommend a policy that isn't included in your policy files.  If you don't think that any of these polocies are a good fit for the customer say so.....")

st.subheader("Question & Answer Assistant")

st.write(":blue[Sample Instructions:] You are an insurance customer service assistant.  You clearly and concisely answer customer questions related to \
         the fourteen insurance policies attached to this chat.  I have provided the file name for each policy below......  \
         \n\n :blue[Constraints:] You only answer questions from the policies attached to this chat.  If you receive a question that is not related to the fourteen insurance polices you politely decline to answer.....")



st.header("Tech Stack")

image = Image.open('image/webapp_workflow.png')
st.image(image, caption='Webapp Workflow')

    
st.header("Q&A")
image = Image.open('image/questions.png')
st.image(image)


    

 
