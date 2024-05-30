import os
from typing import Any, Dict

from pydantic import BaseModel, SecretStr, ValidationError

from .llm import LLMConfig
from .secrets import SecretConfig


class ConfigurationsManager:
    ENV_KEYS = {
        "llm__temperature": "LLM_TEMPERATURE",
        "secret__some_key": "SECRET_SOME_KEY"
    }

    class ConfigModel(BaseModel):
        llm: LLMConfig = LLMConfig()
        secret: SecretConfig = SecretConfig(some_key=SecretStr("default_secret"))

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
