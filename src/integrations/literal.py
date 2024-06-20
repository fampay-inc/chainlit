from literalai import LiteralClient

from src.managers.configs import ConfigurationsManager

config_manager = ConfigurationsManager()


class LiteralAI:
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            api_key = config_manager.config.secret.literal_api_key
            cls.client = LiteralClient(api_key=api_key)

        return cls.client
