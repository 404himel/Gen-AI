import os
import re
import pandas as pd
import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


st.set_page_config(page_title="📘 PDF Q&A Generator", page_icon="🤖", layout="wide")
st.title("📘 PDF Question–Answer Generator (GORQ + RAG)")

st.markdown("""
Welcome! Upload a PDF and ask questions about its content. 
The system will generate answers and save all Q&A pairs as a CSV.
""")


st.sidebar.header("🔑 API Settings")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Stop execution if API key is missing
if not groq_api_key or groq_api_key.strip() == "":
    st.warning("⚠️ Please enter your Groq API Key to proceed.")
    st.stop()  

try:
    groq_api_key = groq_api_key.strip()
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key, temperature=0)
    
    # Test call: ask a trivial question
    response = llm.invoke("Hello")
    
except Exception as e:
    st.error(f"❌ Invalid Groq API Key or connection error: {e}")
    st.stop()


uploaded_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])
if not uploaded_file:
    st.info("Please upload a PDF file to begin.")
    st.stop()


if "processed" not in st.session_state:
    with st.spinner("📚 Loading and splitting PDF..."):
        pdf_path = os.path.join("temp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        texts = splitter.split_documents(documents)

        embedding = OllamaEmbeddings(model="mxbai-embed-large")
        vectorstore = Chroma.from_documents(documents=texts, embedding=embedding)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        st.session_state["retriever"] = retriever
        st.session_state["texts"] = texts
        st.session_state["processed"] = True

st.success(f"✅ Processed {len(st.session_state['texts'])} text chunks from your PDF.")


system_prompt = (
    "You are an intelligent question–answer generation assistant. "
    "Your task is to read the provided text content (retrieved from a PDF document) "
    "and create meaningful, diverse, and contextually accurate question–answer pairs.\n\n"
    "Follow these rules strictly:\n"
    "1. Generate clear and concise questions based only on the given text.\n"
    "2. Each question must be answerable from the context — do not invent facts.\n"
    "3. Write the corresponding answer immediately after each question.\n"
    "4. Prefer factual, conceptual, or reasoning-based questions rather than trivial ones.\n"
    "5. Output format must be clean and structured like this:\n\n"
    "Q1: <question text>\n"
    "A1: <answer text>\n\n"
    "Q2: <question text>\n"
    "A2: <answer text>\n\n"
    "6. If the text contains multiple sections, cover all major ideas fairly.\n"
    "7. Avoid repeating the same type of question; vary the question style (factual, analytical, summary, etc.).\n\n"
    "Your output should only include the question–answer pairs. Do not add explanations or comments.\n\n"
    "Here is the context:\n\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}")
])


llm = ChatGroq(model="llama-3.1-8b-instant",
               api_key=groq_api_key, temperature=0.7)
parser = StrOutputParser()


def create_rag_chain(retriever, model, prompt):
    def fetch_context(user_input):
        docs = retriever.get_relevant_documents(user_input)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"context": context, "question": user_input}

    chain = fetch_context | prompt | model | parser
    return chain

rag_chain = create_rag_chain(st.session_state["retriever"], llm, prompt)


def parse_qa_pairs(model_output):
    pattern = r"Q\d+:\s*(.*?)\nA\d+:\s*(.*?)(?=\nQ\d+:|\Z)"
    matches = re.findall(pattern, model_output, re.DOTALL)
    return [{"Question": q.strip(), "Answer": a.strip()} for q, a in matches]


st.subheader("💬 Ask Questions from the PDF")
user_question = st.text_input("Enter your question or request Q&A generation:")

if "qa_data" not in st.session_state:
    st.session_state.qa_data = []

if st.button("Generate Answer") and user_question.strip():
    with st.spinner("🤖 Generating answer..."):
        rag_chain = create_rag_chain(st.session_state["retriever"], llm, prompt)
        model_output = rag_chain.invoke({"question": user_question})

        # Parse Q&A pairs
        parsed_qa = parse_qa_pairs(model_output)
        st.session_state.qa_data.extend(parsed_qa)

        for i, item in enumerate(parsed_qa, start=1):
            question = item.get("Question", "No Question Found")
            answer = item.get("Answer", "No Answer Found")
            st.markdown(f"**Q{i}:** {question}")
            st.markdown(f"**A{i}:** {answer}")
            st.markdown("---")  # separator between Q&A




if st.session_state.qa_data:
    df = pd.DataFrame(st.session_state.qa_data)
    st.download_button(
        label="📥 Download Q&A CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="qa_results.csv",
        mime="text/csv"
    )
