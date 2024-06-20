from pydantic import BaseModel, Field, StrictStr, StrictInt


class LLMConfig(BaseModel):
    temperature: float = Field(default=0.5, description="Temperature setting for the LLM")
    model_name: StrictStr = Field(default="gpt-3.5-turbo", description="Model name for the LLM")
    max_tokens: StrictInt = Field(default=100, description="Maximum tokens to generate for the LLM")

    # https://platform.openai.com/docs/guides/embeddings/embedding-models
    embedding_model_name: StrictStr = Field(default="text-embedding-3-small", description="Model name for the LLM")
    document_as_rag_source: StrictStr = Field(default="knowledgebase.md", description="Path to the live source file")

    # chat configurations
    chat_history_length: int = Field(default=3, description="Number of chat history messages to pass as context")
    rag_context_length: int = Field(default=3, description="Number of context messages to pass to RAG")
