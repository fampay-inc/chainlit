import os
from typing import Any, Dict

from pydantic import BaseModel, ValidationError

from .llm import LLMConfig
from .secrets import SecretConfig


class ConfigurationsManager:
    ENV_KEYS = {
        "secret__api_key": "API_KEY",
        "secret__api_endpoint": "API_ENDPOINT",
        "secret__api_version": "API_VERSION",
        "secret__api_deployment": "API_DEPLOYMENT",
        "secret__embedding_deployment": "EMBEDDING_DEPLOYMENT",
        "secret__tf_key": "TF_KEY",
        "secret__tf_team_id": "TF_TEAM_ID",
        "secret__tf_proj_id": "TF_PROJ_ID",
        "secret__tf_ds_id": "TF_DS_ID",
        
        "secret__literal_api_key": "LITERAL_API_KEY_CUSTOM",
        "secret__db_conn_str": "DB_CONN",

        "llm__temperature": "LLM_TEMPERATURE",
        "llm__model_name": "LLM_MODEL_NAME",
        "llm__max_tokens": "LLM_MAX_TOKENS",
        "llm__embedding_model_name": "LLM_EMBEDDING_MODEL_NAME",
        "llm__document_as_rag_source": "LLM_DOCUMENT_AS_RAG_SOURCE",
        "llm__chat_history_length": "LLM_CHAT_HISTORY_LENGTH",
        "llm__rag_context_length": "LLM_RAG_CONTEXT_LENGTH",
    }

    class ConfigModel(BaseModel):
        llm: LLMConfig = LLMConfig()
        secret: SecretConfig = SecretConfig()

    def __init__(self):
        self._load_config()

    def _load_config(self):
        env_vars = self._extract_env_vars()
        try:
            self.config = self.ConfigModel(**env_vars)
        except ValidationError as e:
            raise ValueError(f"Configuration validation error: {e}")

    def _extract_env_vars(self) -> Dict[str, Any]:
        env_vars = {}
        for attr_path, env_key in self.ENV_KEYS.items():
            env_value = os.getenv(env_key)
            if env_value is not None:
                keys = attr_path.split('__')
                self._set_nested_dict_value(env_vars, keys, env_value)
        return env_vars

    def _set_nested_dict_value(self, dict_: Dict[str, Any], keys: list, value: Any):
        for key in keys[:-1]:
            dict_ = dict_.setdefault(key, {})
        dict_[keys[-1]] = value

    def __getattr__(self, item: str) -> Any:
        if hasattr(self.config, item):
            return getattr(self.config, item)
        raise AttributeError(f"'ConfigurationsManager' object has no attribute '{item}'")
