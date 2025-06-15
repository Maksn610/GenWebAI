from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

class MemoryManager:
    def __init__(self):
        self.sessions = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.sessions:
            self.sessions[session_id] = InMemoryChatMessageHistory()
        return self.sessions[session_id]

memory_manager = MemoryManager()
