from .base import BaseChatHistoryManager


class InMemoryChatHistoryManager(BaseChatHistoryManager):
    def __init__(self):
        self.chat_history = []

    def add_chat(self, role: str, content: str):
        """Saves actor's message into history"""
        self.chat_history.append({
            "role": role,
            "content": content
        })

    def save_user_message(self, content: str):
        self.add_chat("user", content)

    def save_assistant_message(self, content: str):
        self.add_chat("assistant", content)

    def save_system_message(self, content: str):
        self.add_chat("system", content)

    def get_last_message(self):
        """Returns the last message in the chat history, if any"""
        if len(self.chat_history) == 0:
            return None
        return self.chat_history[-1]

    def get_last_n_messages(self, n: int):
        """Returns the last n messages in the chat history"""
        return self.chat_history[-n:]

    def get_last_n_messages_by(self, role: str, n: int):
        """Returns the last n messages by the actor in the chat history"""
        actor_messages = [chat for chat in self.chat_history if chat["role"] == role]
        return actor_messages[-n:]
