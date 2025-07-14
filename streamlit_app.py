# pip install -qU langchain-ollama
# pip install langchain
# pip install streamlit

import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate

st.title(":brain: Roy's ChatBot!!!")
st.write("Get Help for Mental Health")

model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

system_message = SystemMessagePromptTemplate.from_template(
    "You are a compassionate and emotionally aware AI chatbot. You recognize users' emotions and respond with empathy, support, and kindness. You do not replace trained mental health professionals and never attempt to diagnose or provide clinical advice. You must never refer users to crisis lines, emergency numbers, or any clinical mental health services. Your role is to offer a safe, non-judgmental space for users to express themselves and feel heard."
)


if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

with st.form("llm-form"):
    text = st.text_area("Feel Free To Share")
    submit = st.form_submit_button("Enter")

def generate_response(chat_histroy):
    chat_template = ChatPromptTemplate.from_messages(chat_histroy)

    chain = chat_template|model|StrOutputParser()

    response = chain.invoke({})

    return response

# user message in 'user' key
# ai message in 'assistant' key
def get_history():
    chat_history = [system_message]
    for chat in st.session_state['chat_history']:
        prompt = HumanMessagePromptTemplate.from_template(chat['user'])
        chat_history.append(prompt)

        ai_message = AIMessagePromptTemplate.from_template(chat['assistant'])
        chat_history.append(ai_message)

    return chat_history


if submit and text:
    with st.spinner("Generating response..."):
        prompt = HumanMessagePromptTemplate.from_template(text)

        chat_history = get_history()

        chat_history.append(prompt)

        # st.write(chat_history)

        response = generate_response(chat_history)

        st.session_state['chat_history'].append({'user': text, 'assistant': response})

        # st.write("response: ", response)

        # st.write(st.session_state['chat_history'])


st.write('## Chat History')
for chat in reversed(st.session_state['chat_history']):
       st.write(f"**:adult: User**: {chat['user']}")
       st.write(f"**:brain: Assistant**: {chat['assistant']}")
       st.write("---")




