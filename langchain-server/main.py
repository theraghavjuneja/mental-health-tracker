import streamlit as st
import os
import uuid  
from text import return_top_message_text
from backend.app import give_output,suggest_songs,suggest_podcast

st.header("Mental Health Chatbot")

with st.expander("ℹ️ Disclaimer"):
    st.caption("""
        This mental health chatbot depicts your current state based on the conversations you are having.
        For each user, it would be outputting different things depending on their state based on the conversations. After some time, 
        when we have enough information about you this can also help you suggest songs, podcasts, YouTube videos, etc., based on how you are feeling."""
            )
st.info("Please refrain from using any of the Resources like Suggest some songs without talking to bot. Since we need some information before suggesting content")
project_id = "hackathon-chatbot-tx9j"

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
CONVERSATION_HISTORY = "conversation_history"
SESSION_ID = "session_id"

def generate_session_id():
    if SESSION_ID not in st.session_state:
        st.session_state[SESSION_ID] = str(uuid.uuid4())

def initialize_session():
    generate_session_id() 
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

def return_message(session_id, message):
    response = give_output(sessionId=session_id, human_message=message)
    return response

def show_new_window(title, content):
    st.session_state["window_title"] = title
    st.session_state["window_content"] = content

def render_new_window():
    if "window_title" in st.session_state and "window_content" in st.session_state:
        st.subheader(st.session_state["window_title"])
        st.write(st.session_state["window_content"])



# Convert chat history to a single string
def get_conversation_as_string():
    conversation = st.session_state[MESSAGES]
    conversation_str = "\n".join([f"{msg['actor']}: {msg['payload']}" for msg in conversation])
    return conversation_str

# Sidebar buttons with actions
def sidebar_buttons():
    with st.sidebar:
        st.markdown("---")
        st.subheader("Resources")
        
        if st.button("🎵 Suggest me some songs"):
           
            conversation_str = get_conversation_as_string()
            song_suggestions = suggest_songs(conversation_str)  
            show_new_window("Song Suggestions", song_suggestions)  
        
        if st.button("🎙️ Suggest some podcasts"):
            conversation_str=get_conversation_as_string()
            podcast_suggestion=suggest_podcast(conversation_str)
            show_new_window("Podcast suggestions",podcast_suggestion)
        
        if st.button("🧑‍⚕️ Find therapists near me"):
            show_new_window("Find Therapists", "Here are some resources to find therapists near you:\n- Resource 1\n- Resource 2\n- Resource 3")
        
        if st.button("🌐 Suggest online resources"):
            show_new_window("Online Resources", "Here are some useful online mental health resources:\n- Resource 1\n- Resource 2\n- Resource 3")
        
        if st.button("📝 Take Depression Test"):
            show_new_window("Depression Test", "You can take a self-assessment depression test here:\n- Test 1\n- Test 2")

def main():
    initialize_session()  
    with st.sidebar:
        if st.button("🆕 New Chat"):
            reset_chat()

    view_chat_history()  
    display_messages(st.session_state[MESSAGES])  

    # Sidebar buttons are always visible
    sidebar_buttons()

    # Accept user input
    prompt = st.chat_input("I'm your mental health assistant, Please ask whatever you need to ask")
    
    # Render new window content based on button clicks
    render_new_window()

    if prompt:
        user_message = {"actor": USER, "payload": prompt}
        st.session_state[MESSAGES].append(user_message)
        st.chat_message(USER).write(prompt)

        response = return_message(st.session_state[SESSION_ID], prompt)
        assistant_message = {"actor": ASSISTANT, "payload": response}
        st.session_state[MESSAGES].append(assistant_message)
        st.chat_message(ASSISTANT).write(response)

if __name__ == "__main__":
    main()
