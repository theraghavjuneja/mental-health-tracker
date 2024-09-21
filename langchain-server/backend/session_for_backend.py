import os
import json
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

HISTORY_DIR = "session_histories"

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def get_session_file(session_id: str) -> str:
    """Get the file path for storing session history."""
    return os.path.join(HISTORY_DIR, f"{session_id}_history.json")

def load_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Load the session history from a file."""
    session_file = get_session_file(session_id)
    chat_history = InMemoryChatMessageHistory()
    
    if os.path.exists(session_file):
        with open(session_file, 'r') as file:
            history_data = json.load(file)
            for entry in history_data:
                chat_history.add_message(entry)  # Assuming entry is a simple string or dict.
    
    return chat_history

def save_session_history(session_id: str, chat_history: InMemoryChatMessageHistory):
    """Save the session history to a file."""
    session_file = get_session_file(session_id)
    history_data = [msg for msg in chat_history.messages]  # Assuming messages are directly serializable.

    with open(session_file, 'w') as file:
        json.dump(history_data, file)

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieve or create a session history."""
    return load_session_history(session_id)

def update_session_history(session_id: str, message: str):
    """Add a message to the session history and save it."""
    chat_history = get_session_history(session_id)
    chat_history.add_message(message)  # Assuming message is a string.
    save_session_history(session_id, chat_history)

if __name__=='__main__':
    session_id = "12345"
    update_session_history(session_id, "Hello, how can I assist you?")
    history = get_session_history(session_id)
    print(history.messages)  # This will print the stored messages
