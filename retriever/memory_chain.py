def get_retriver(vector_store):
    return vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})