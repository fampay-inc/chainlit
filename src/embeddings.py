from chromadb import Chroma
from chroma import Chroma

def create_embeddings(database_path, documents, embeddings_model):
    db = Chroma.from_documents(documents, embeddings_model, persist_directory=database_path)
    db.persist()
    return db


def create_combined_embeddings(database_path, documents_1, documents_2, embeddings_model):
    db = Chroma(embedding_function=embeddings_model, persist_directory=database_path)
    db.add_documents(documents_1)
    db.add_documents(documents_2)
    db.persist()
    return db


def load_embeddings(database_path, embeddings_model):
    db = Chroma(persist_directory=database_path, embedding_function=embeddings_model)
    return db


def update_embeddings(database_path, documents, embeddings_model):
    db_org = load_embeddings(database_path, embeddings_model)
    db_new = Chroma.from_documents(documents, embeddings_model)
    db_new_data = db_new._collection.get(include=['documents', 'metadatas', 'embeddings'])
    db_org._collection.add(
        embeddings=db_new_data['embeddings'],
        metadatas=db_new_data['metadatas'],
        documents=db_new_data['documents'],
        ids=db_new_data['ids']
    )
    db_org.persist()
    return db_org