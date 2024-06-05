import logging
from typing import Optional

import chainlit

from src.llm import LLM
from src.managers.chat_hisory import InMemoryChatHistoryManager
from src.managers.configs import ConfigurationsManager
from src.managers.prompt.PromptManager import PromptManager
from src.vector_storage.chroma import ChromaVectorManager
from src.tf_logging import track_tensorfuse_log

LOGGER = logging.getLogger(__name__)

llm = LLM()
config_manager = ConfigurationsManager()
vector_storage = ChromaVectorManager(llm)


@chainlit.oauth_callback
def oauth_callback(
        provider_id: str,
        token: str,
        raw_user_data,
        default_user,
) -> Optional[chainlit.User]:
    allowed_domains = ["fampay.in", "triotech.co.in", ]
    allowed_emails = []
    if provider_id == "google":
        user_email = raw_user_data["email"]
        user_domain = user_email.split('@')[-1]

        if user_email in allowed_emails or user_domain in allowed_domains:
            return default_user

    return None


@chainlit.on_chat_start
async def on_chat_start_handler():
    """
    Run once when the chat session starts for each user
    """
    memory = InMemoryChatHistoryManager()
    # memory.add_chat("system", "You are a helpful assistant.")
    chainlit.user_session.set("memory", memory)

    await chainlit.Avatar(
        name="Fam",
        url="./public/favicon.ico",
    ).send()


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

    # get related documents from user's message
    users_message_vector = llm.get_embedding(user_message)

    rag_count = config_manager.config.llm.rag_context_length
    raw_related_docs = vector_storage.get_related_documents(users_message_vector, rag_count)
    related_docs = vector_storage.transform_rag_output_into_str(raw_related_docs)

    chat_history_length = config_manager.config.llm.chat_history_length
    chat_ctx = memory.get_last_n_messages(chat_history_length)

    prompt_ctx = PromptManager.generate_messages_prompt(related_docs, chat_ctx)
    completion = llm.get_chat_completion(prompt_ctx)

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

    # TensorFuse Logging
    log = {
        "input": user_message,
        "output": ai_response.content,
        "source_docs": related_docs
    }

    track_tensorfuse_log(log)
    


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
