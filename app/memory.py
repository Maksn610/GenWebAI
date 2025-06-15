from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import Dict

class MemoryManager:
    def __init__(self):
        self.histories: Dict[str, InMemoryChatMessageHistory] = {}

    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self.histories:
            self.histories[session_id] = InMemoryChatMessageHistory()
        return self.histories[session_id]

memory_manager = MemoryManager()
