from .base import BaseChatHistoryManager


class InMemoryChatHistoryManager(BaseChatHistoryManager):
    def __init__(self):
        self.chat_history = []

    def add_chat(self, actor: str, message: str):
        """Saves actor's message into history"""
        self.chat_history.append({
            "actor": actor,
            "message": message
        })

    def get_last_message(self):
        """Returns the last message in the chat history, if any"""
        if len(self.chat_history) == 0:
            return None
        return self.chat_history[-1]

    def get_last_n_messages(self, n: int):
        """Returns the last n messages in the chat history"""
        return self.chat_history[-n:]

    def get_last_n_messages_by(self, actor: str, n: int):
        """Returns the last n messages by the actor in the chat history"""
        actor_messages = [chat for chat in self.chat_history if chat["actor"] == actor]
        return actor_messages[-n:]
