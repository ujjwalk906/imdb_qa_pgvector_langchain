from langchain_postgres import PGVector

def get_vector_store(embeddings, conn_str: str, collection_name="movies"):
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=conn_str,
        use_jsonb=True
    )

def add_documents_to_store(vector_store, docs):
    ids = [str(i) for i in range(1,len(docs)+1)]
    vector_store.add_documents(docs, ids=ids)