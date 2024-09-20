import streamlit as st
import os
from static.text import return_top_message_text

st.header("Mental Health Chatbot")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        return_top_message_text
    )


def return_message(project_id, session_id, message):  
    return "Hello World"

project_id = "hackathon-chatbot-tx9j"
session_id = "my_id"
USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
CONVERSATION_HISTORY = "conversation_history"

def initialize_session():
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = []
    
    if CONVERSATION_HISTORY not in st.session_state:
        st.session_state[CONVERSATION_HISTORY] = []  

def display_messages(messages):
    for msg in messages:
        st.chat_message(msg["actor"]).write(msg["payload"])

def reset_chat():
    if st.session_state[MESSAGES]:
        st.session_state[CONVERSATION_HISTORY].append(st.session_state[MESSAGES])
    st.session_state[MESSAGES] = []

def view_chat_history():
    with st.sidebar:
        st.subheader("Chat History")
        if st.session_state[CONVERSATION_HISTORY]:
            for idx, conversation in enumerate(st.session_state[CONVERSATION_HISTORY]):
                if st.button(f"Conversation {idx + 1}"):
                    st.session_state[MESSAGES] = conversation  
                    st.experimental_rerun()  
        else:
            st.write("No previous conversations")

def main():
    initialize_session()
    with st.sidebar:
        if st.button("🆕 New Chat"):
            reset_chat()
    view_chat_history() 
    display_messages(st.session_state[MESSAGES]) 
    prompt = st.chat_input("Enter a prompt here.")
    if prompt:
        user_message = {"actor": USER, "payload": prompt}
        st.session_state[MESSAGES].append(user_message)
        st.chat_message(USER).write(prompt)
        response = return_message(project_id, session_id, prompt) 
        assistant_message = {"actor": ASSISTANT, "payload": response}
        st.session_state[MESSAGES].append(assistant_message)
        st.chat_message(ASSISTANT).write(response)

if __name__ == "__main__":
    main()
