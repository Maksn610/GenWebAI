from app.memory import memory_manager
from langchain_core.chat_history import InMemoryChatMessageHistory

def test_get_session_history_new():
    session_id = "test-session"
    history = memory_manager.get_session_history(session_id)
    assert isinstance(history, InMemoryChatMessageHistory)

def test_get_session_history_same_instance():
    session_id = "same-session"
    first = memory_manager.get_session_history(session_id)
    second = memory_manager.get_session_history(session_id)
    assert first is second
