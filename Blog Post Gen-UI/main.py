import streamlit as st 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv 
import os 
from groq import Groq
load_dotenv()

load_env = os.getenv("gorq_api_key")

model = ChatGroq(model="llama-3.1-8b-instant",
                    api_key=load_env, temperature=0.7)

system_prompt = (
    "You are a helpful assistant that helps people find information about blog post generation."
    " Provide clear and concise answers to user queries."
    " If you don't know the answer, respond with 'I'm sorry, I don't have that information at the moment.'"
    "\n\n"
)   
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}"),
])

# chain = prompt | model
# response = chain.invoke({"question":"How to generate a blog post using AI?"})

def check_api_key(key):
    try:
        groq_client = Groq(api_key=key)
        models = groq_client.models.list()
        print(models)
        print(models)
        return True
    except Exception as e:
        return False
    

## UI with Streamlit

st.title("Blog Post Generation Assistant 🤖📝")

st.markdown("Enter your GORQ API Key to get started.")



api_key = st.text_input("GORQ API Key", type="password")

st.markdown("Status:")
if api_key:
    try:
        check_api_key(api_key)
        st.success("✅ Valid API Key!")
    except Exception as e:
        st.error(f"❌ Invalid. Error: {e}")



st.markdown("Ask me anything about blog post generation!")

user_question = st.text_input("Your Question:")

if user_question and api_key and check_api_key(api_key):
    model = ChatGroq(model="llama-3.1-8b-instant",
                    api_key=api_key, temperature=0.7)
    chain = prompt | model
    response = chain.invoke({"question": user_question})
    st.markdown("Your Blog Post Generation Assistant's Response: ")
    st.write(response.content)




