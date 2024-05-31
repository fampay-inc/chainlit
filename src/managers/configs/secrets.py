from pydantic import BaseModel, Field, StrictStr


class SecretConfig(BaseModel):
    api_key: StrictStr = Field("secret-open-api-key", description="API key")
    api_endpoint: StrictStr = Field("secret-azure-endpoint", description="Azure endpoint")
    api_version: StrictStr = Field("secret-api-version", description="API version")
    api_deployment: StrictStr = Field("secret-azure-deployment", description="Azure deployment")
    embedding_deployment: StrictStr = Field("secret-embedding-deployment", description="Embedding deployment")
