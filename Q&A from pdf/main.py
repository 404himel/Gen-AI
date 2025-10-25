from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate 
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser




load_dotenv()


file_path = "/home/himel/Documents/Level 01 App/Q&A from pdf/bang.pdf"

loader = PyPDFLoader(file_path)

document = loader.load()

load_env = os.getenv("gorq_api_key")

# print(document[0].page_content[0:1000])
# print(document[0].metadata)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

texts = text_splitter.split_documents(document)

# print(f"Number of documents: {len(texts)}")


embeddings = OllamaEmbeddings(model="mxbai-embed-large")
vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

retriver = vectorstore.as_retriever()


model = ChatGroq(model="llama-3.1-8b-instant",
                    api_key=load_env, temperature=0.7)
system_prompt = (
    "You are a knowledgeable assistant specialized in answering questions based on provided document excerpts."
    " Use the context to provide accurate and concise answers."
    " If the context does not contain the answer, respond with 'The provided document does not contain the information requested.'"
    "answer concisely."
    "answer in english language."
    "\n\n"
    "{context}"
)


prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}"),
])

# qa_chain = create_stuff_documents_chain(model, prompt)

# rag_chain = create_retrieval_chain(retriver, qa_chain)


def create_pipe_rag_chain(retriever, model, prompt):

        def fetch_context(user_input):
            docs = retriever.get_relevant_documents(user_input)
            context_text = "\n\n".join(doc.page_content for doc in docs)
            return {"context": context_text, "question": user_input}
        
        rag_chain = (
            fetch_context      
            | prompt           
            | model            
            | StrOutputParser() 
        )
        
        return rag_chain



rag_chain = create_pipe_rag_chain(retriver, model, prompt)

def chat():
    print("🤖 Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("🧑 You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye! 👋")
            return

        response = rag_chain.invoke({"question": user_input})

        print("🤖:", response)



if __name__ == "__main__":
    chat()