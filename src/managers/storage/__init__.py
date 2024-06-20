from chainlit.data import BaseStorageClient
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

from src.managers.configs import ConfigurationsManager

config_manager = ConfigurationsManager()


class BypassStorageClient(BaseStorageClient):
    """
    Dummy storage client which does not upload any data to the storage
    """
    pass


class DataLayerManager:
    data_layer = None

    @classmethod
    def get_client(cls):
        if cls.data_layer is None:
            storage_client = BypassStorageClient()
            connection_str = config_manager.config.secret.db_conn_str
            data_layer = SQLAlchemyDataLayer(conninfo=connection_str, storage_provider=storage_client)
            cls.data_layer = data_layer

        return cls.data_layer
