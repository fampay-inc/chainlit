import logging

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from src.llm import LLM
from src.managers.configs import ConfigurationsManager
from src.vector_storage.utils import get_text_from_file

config_manager = ConfigurationsManager()
delimiter = '------------------------------------------'

LOGGER = logging.getLogger(__name__)


class ChromaVectorManager:
    vector_collection = None

    def __init__(self, llm_client: LLM):
        self.llm_client = llm_client
        self.vector_client = chromadb.PersistentClient(path="./data/processed")

    def create_collection(self, identifier):
        embedding_model = config_manager.config.llm.embedding_model_name
        collection_name = f"{embedding_model}-{identifier}"
        self.vector_client.create_collection(collection_name)

    def generate_document_embeddings(self):
        identifier = config_manager.config.llm.document_as_rag_source
        path = f"./data/documents/{identifier}"

        text_content = get_text_from_file(path)
        chunks = text_content.split(delimiter)
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        self.create_and_store_embeddings(identifier, chunks)

    def create_and_store_embeddings(self, identifier: str, chunks: list):
        self.create_collection(identifier)

        embedding_model = config_manager.config.llm.embedding_model_name
        embedding_function = OpenAIEmbeddingFunction(
            api_key=config_manager.config.secret.api_key,
            model_name=embedding_model,
        )

        collection_name = f"{embedding_model}-{identifier}"
        vector_collection = self.vector_client.get_collection(
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
            print(f"Progress: {i}/{len(chunks)}, Percent: {i / len(chunks) * 100}%")

    def get_related_documents(self, search_vector: any, k: int = 2):
        identifier = config_manager.config.llm.document_as_rag_source
        embedding_model = config_manager.config.llm.embedding_model_name
        collection_name = f"{embedding_model}-{identifier}"

        vector_collection = self.vector_client.get_collection(collection_name)
        response = vector_collection.query(
            query_embeddings=search_vector,
            n_results=k,
            include=["metadatas"],
        )
        return response

    @staticmethod
    def transform_rag_output_into_str(rag_output) -> str:
        output = []

        for doc in rag_output['metadatas'][0]:
            txt = doc['text']
            txt = txt.replace("--", "")
            txt = txt.replace("  ", " ")
            txt = txt.strip()
            txt = txt.replace("Q:", "\nQ:")

            output.append(txt)

        return "".join(output)


"""
Directly execute this file to generate embeddings
"""
if __name__ == "__main__":
    llm_client = LLM()
    x = ChromaVectorManager(llm_client)
    x.generate_document_embeddings()

    search_string = llm_client.get_embedding("camera")
    raw_response = x.get_related_documents(search_string, 3)
    response = x.transform_rag_output_into_str(raw_response)
