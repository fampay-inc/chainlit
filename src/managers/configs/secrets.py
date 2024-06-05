from pydantic import BaseModel, Field, StrictStr


class SecretConfig(BaseModel):
    api_key: StrictStr = Field("secret-open-api-key", description="API key")
    api_endpoint: StrictStr = Field("secret-azure-endpoint", description="Azure endpoint")
    api_version: StrictStr = Field("secret-api-version", description="API version")
    api_deployment: StrictStr = Field("secret-azure-deployment", description="Azure deployment")
    embedding_deployment: StrictStr = Field("secret-embedding-deployment", description="Embedding deployment")
    tf_key: StrictStr = Field("secret-tensorfuse-key", description="TensorFuse API Key")
    tf_team_id: StrictStr = Field("secret-tensorfuse-team-id", description="TensorFuse Team ID")
    tf_proj_id: StrictStr = Field("secret-tensorfuse-proj-id", description="TensorFuse Project ID")
    tf_ds_id: StrictStr = Field("secret-tensorfuse-ds-id", description="TensorFuse Datasource ID")
    
