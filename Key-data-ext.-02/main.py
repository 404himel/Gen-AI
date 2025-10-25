from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

load_env = os.getenv("gorq_api_key")
class Person(BaseModel):
    
    name : Optional[str] = Field(None, description="Name of the person")

    age : Optional[int] = Field(None, description="Age of the person")

    country : Optional[str] = Field(None, description="Country of the person")


class Data(BaseModel):
    People: list[Person] = Field(..., description="List of people extracted from the text")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert extraction algorithm."
     "Only extract relevant information from the text"
     "If you don't find any relevant information, respond with 'No relevant information found.'"),
     ("user", "{input}"),
])

model = ChatGroq(model="llama-3.1-8b-instant",
                 api_key=load_env, temperature=0.7)

chain = prompt | model.with_structured_output(Data)

def chat():
    print("🤖 Chatbot is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("🧑 You: ").strip()
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye! 👋")
            return
        response = chain.invoke({
            "input": user_input
        })

        print("🤖:", response)


if __name__ == "__main__":
    chat()