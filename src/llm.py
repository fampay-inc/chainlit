from openai import AzureOpenAI

from src.managers.configs import ConfigurationsManager

config_manager = ConfigurationsManager()


class LLM:
    llm_client = None
    embedding_client = None

    @classmethod
    def get_chat_client(cls):
        if cls.llm_client is None:
            cls.llm_client = AzureOpenAI(
                api_key=config_manager.config.secret.api_key,
                azure_endpoint=config_manager.config.secret.api_endpoint,
                api_version=config_manager.config.secret.api_version,
                azure_deployment=config_manager.config.secret.api_deployment,
            )

        return cls.llm_client

    @classmethod
    def get_embedding_client(cls):
        if cls.embedding_client is None:
            cls.embedding_client = AzureOpenAI(
                api_key=config_manager.config.secret.api_key,
                azure_endpoint=config_manager.config.secret.api_endpoint,
                api_version=config_manager.config.secret.api_version,
                azure_deployment=config_manager.config.secret.embedding_deployment,
            )

        return cls.embedding_client

    @classmethod
    def get_chat_completion(cls, messages):
        client = cls.get_chat_client()

        return client.chat.completions.create(
            model=config_manager.config.llm.model_name,
            max_tokens=config_manager.config.llm.max_tokens,
            stream=True,
            messages=messages,
        )

    @classmethod
    def get_embedding(cls, chunk: str):
        client = cls.get_embedding_client()

        response = client.embeddings.create(
            input=chunk,
            model=config_manager.config.llm.embedding_model_name,
        )
        return response.data[0].embedding
