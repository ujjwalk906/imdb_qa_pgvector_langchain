from langchain_openai import OpenAIEmbeddings

def load_embedding_model():
    return OpenAIEmbeddings(model="text-embedding-3-small")