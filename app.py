# app.py

import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# Title and description
st.title(":brain: Roy's ChatBot!!!")
st.write("Get help for mental health")

# Optional: Set API key locally if running outside Render
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# GPT-3.5 Turbo with moderate creativity
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# System behavior
system_message = SystemMessage(
    content=(
        "You are a compassionate AI mental health assistant trained to detect emotional cues in user messages "
        "and respond with empathy, understanding, and support. "
        "You never offer clinical diagnoses or medical advice. "
        "You encourage users gently, validate their feelings, and offer positive coping suggestions when appropriate."
    )
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input form
with st.form("llm-form"):
    text = st.text_area("What's on your mind!")
    submit = st.form_submit_button("Enter")

# Function to prepare full chat history
def get_history():
    chat_history = [system_message]
    for chat in st.session_state["chat_history"]:
        chat_history.append(HumanMessage(content=chat["You"]))
        chat_history.append(AIMessage(content=chat["AI Assistant"]))
    return chat_history

# Generate AI response
def generate_response(chat_history):
    chain = model | StrOutputParser()
    response = chain.invoke(chat_history)
    return response

# Process form submission
if submit and text:
    with st.spinner("Generating response..."):
        chat_history = get_history()
        chat_history.append(HumanMessage(content=text))
        response = generate_response(chat_history)
        st.session_state["chat_history"].append({"You": text, "AI Assistant": response})

# Display chat history
st.write("## Chat History")
for chat in reversed(st.session_state["chat_history"]):
    st.write(f"**:adult: You**: {chat['You']}")
    st.write(f"**:brain: AI Assistant**: {chat['AI Assistant']}")
    st.write("---")
