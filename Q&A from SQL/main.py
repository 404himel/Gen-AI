from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase 
from langchain_community.chains import create_sql_query_chain



load_dotenv()
load_env = os.getenv("gorq_api_key")

model = ChatGroq(model="llama-3.1-8b-instant",
                    api_key=load_env, temperature=0.7)



#after create the database(.sql) then run this command in terminal (sqlite3 db_name.db < db_name.sql) to create the database
db_path = "/home/himel/Documents/Level 01 App/Q&A from SQL/students.db"

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

chain = create_sql_query_chain(model, db)

def chat():
    print("🤖 Chatbot is ready! Type 'exit' to quit.\n")

    def extract_sql(response_text):
        """
        Extract only the SQL query from the response text.
        Assumes the line starts with 'SQLQuery: '
        """
        lines = response_text.splitlines()
        for line in lines:
            if line.startswith("SQLQuery:"):
                # Remove 'SQLQuery:' and any leading/trailing spaces
                return line.replace("SQLQuery:", "").strip()
        return None

    while True:
        user_input = input("🧑 You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye! 👋")
            return

        # Invoke the chain with correct key
        response = chain.invoke({"question": user_input})

        # Extract only the SQL query
        sql_query = extract_sql(response)
        if sql_query:
            print("🤖: Extracted SQL Query:\n", sql_query)
            try:
                output = db.run(sql_query)
                print("🤖: The Answer is:", output)
            except Exception as e:
                print("🤖: Error running SQL query:", e)
        else:
            print("🤖: Could not extract a valid SQL query from the response.")


if __name__ == "__main__":
    chat()