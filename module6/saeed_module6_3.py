pip install streamlit langchain langchain-openai chromadb python-docx

import streamlit as st
import sqlite3
from datetime import datetime
from langchain_openai import ChatOpenAI
import os


DB_FILE = "chat.db"
MODEL_NAME = "gpt-4o-mini"

st.set_page_config(page_title="LLM Chat (SQL Memory)", layout="centered")
st.title("💬 LLM Chat with SQL Memory")


conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT,
    timestamp TEXT
)
""")
conn.commit()


def save_message(role, message):
    cursor.execute(
        "INSERT INTO chat_history (role, message, timestamp) VALUES (?, ?, ?)",
        (role, message, datetime.now().isoformat())
    )
    conn.commit()

def load_messages():
    cursor.execute("SELECT role, message FROM chat_history ORDER BY id")
    return cursor.fetchall()


history = load_messages()

for role, message in history:
    with st.chat_message(role):
        st.markdown(message)


llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=os.getenv("OPENAI_API_KEY")
)

user_input = st.chat_input("Ask your question...")

if user_input:
    
    with st.chat_message("user"):
        st.markdown(user_input)

    save_message("user", user_input)

   
    with st.chat_message("assistant"):
        response = llm.invoke(user_input)
        answer = response.content
        st.markdown(answer)

    save_message("assistant", answer)

if st.button(" Clear Chat History"):
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    st.rerun()
    
