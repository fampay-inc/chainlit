import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from src.llm import LLM
from src.managers.configs import ConfigurationsManager

config_manager = ConfigurationsManager()


class ChromaVectorManager:
    vector_collection = None

    def __init__(self, llm_client: LLM):
        self.llm_client = llm_client
        self.vector_client = chromadb.PersistentClient(path="./embeddings")

    def create_and_store_embeddings(self, identifier: str, chunks: list):
        embedding_model = config_manager.config.llm.embedding_model_name
        embedding_function = OpenAIEmbeddingFunction(
            api_key=config_manager.config.secret.api_key,
            model_name=embedding_model,
        )

        collection_name = f"{embedding_model}-{identifier}"
        vector_collection = self.vector_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
        )

        for i, chunk in enumerate(chunks):
            embedding = self.llm_client.get_embedding(chunk)
            vector_collection.add(
                ids=["doc_%s" % i],
                embeddings=[embedding],
                metadatas=[{"text": chunk}],
            )

    def get_related_documents(self, identifier: str, search_vector: any, k: int = 2):
        embedding_model = config_manager.config.llm.embedding_model_name
        collection_name = f"{embedding_model}-{identifier}"
        vector_collection = self.vector_client.get_collection(collection_name)
        response = vector_collection.query(
            query_embeddings=search_vector,
            n_results=k,
            include=["metadatas"],
        )
        return response


"""
Code to test the ChromaVectorManager class
"""
# llm_client = LLM()
# x = ChromaVectorManager(llm_client)
# x.create_and_store_embeddings("debug", ["earth is a flat planet", "venus is yellow planet", "marks is pink", "apple are red", "earth is blue", "fampay is fintech"])
#
# search_string = llm_client.get_embedding("earth planet")
# response = x.get_related_documents("debug", search_string, 3)
# print(response)
