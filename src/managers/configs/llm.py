from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    temperature: float = Field(default=0.7, description="Temperature setting for the LLM")
