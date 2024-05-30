import chainlit


@chainlit.on_chat_start
async def on_chat_start_handler():
    """
    Run once when the chat session starts for each user
    """
    some_data = {"user": "user's name"}
    chainlit.user_session.set("user_details", some_data)


@chainlit.on_message
async def on_message_handler(message: chainlit.Message):
    """
    Run everytime the user sends a message
    """
    print("> on_message")
    user_message = message.content.lower()
    response = f"Hello, you just sent: {user_message}!"
    await chainlit.Message(response).send()


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
    print("> on_chat_end")
