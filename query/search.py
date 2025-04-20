from langchain_postgres import PGVector

def search_movies(vector_store: PGVector, query, k=5, metadata_filter=None):
    return vector_store.similarity_search(query,k=k, filter=metadata_filter or {})