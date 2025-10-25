from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
import os

load_dotenv()

gorq_api_key = os.getenv("gorq_api_key")

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("User: {input}")
])

memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory("chat_history.json"),
    memory_key="history",
    return_messages=True
)

llm = ChatGroq(
    api_key=gorq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.7
)

chain = prompt | llm 

def chat():
    print("🤖 Chatbot is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye! 👋")
            break

        # Load previous memory
        history_messages = memory.load_memory_variables({})

        # Get model response
        response = chain.invoke({
            "history": history_messages.get("history", []),
            "input": user_input
        })

        # Save context
        memory.save_context({"input": user_input}, {"output": response.content})

        # Print reply
        print("🤖:", response.content)
        print()

# if __name__ == "__main__":
#     chat()
print(memory.chat_memory.messages)