from pydantic import BaseModel, Field, SecretStr


class SecretConfig(BaseModel):
    some_key: SecretStr = Field(..., description="Some secret key")
