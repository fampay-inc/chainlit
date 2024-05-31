import logging

import chainlit

from src.llm import LLM
from src.managers.chat_hisory import InMemoryChatHistoryManager
from src.managers.configs import ConfigurationsManager

LOGGER = logging.getLogger(__name__)

llm = LLM()
config_manager = ConfigurationsManager()


@chainlit.on_chat_start
async def on_chat_start_handler():
    """
    Run once when the chat session starts for each user
    """
    memory = InMemoryChatHistoryManager()
    memory.add_chat("system", "You are a helpful assistant.")
    chainlit.user_session.set("memory", memory)


@chainlit.on_message
async def on_message_handler(message: chainlit.Message):
    """
    Run everytime the user sends a message
    """
    memory: InMemoryChatHistoryManager = chainlit.user_session.get("memory")

    ai_response = chainlit.Message(content="")
    await ai_response.send()

    user_message = message.content.lower()
    memory.save_user_message(user_message)

    conversation_ctx = memory.get_last_n_messages(3)
    completion = llm.get_chat_completion(conversation_ctx)

    for chunk in completion:
        response_length = len(chunk.choices)
        if response_length == 0:
            continue

        if hasattr(chunk.choices[0], "delta"):
            if hasattr(chunk.choices[0].delta, "content"):
                if isinstance(chunk.choices[0].delta.content, str):
                    await ai_response.stream_token(chunk.choices[0].delta.content)

    memory.save_assistant_message(ai_response.content)
    await ai_response.update()


@chainlit.on_stop
def on_stop():
    """
    the user clicks the stop button while a task was running.
    """
    print("> on_stop")


@chainlit.on_chat_end
def on_chat_end():
    """
    the chat session ends either because the user disconnected or started a new chat session.
    """
    LOGGER.info("> Chat Session Ended")
    memory: InMemoryChatHistoryManager = chainlit.user_session.get("memory")
    for x in memory.chat_history:
        LOGGER.info(f"{x['role']}: {x['content']}")
