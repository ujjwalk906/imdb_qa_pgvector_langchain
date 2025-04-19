from config import load_config
from data.load_data import load_sample
from data.preprocess import create_documents
from db.vector_store import get_vector_store, add_documents_to_store
from embedding.embed import load_embedding_model
from query.search import search_movies
from query.summarize import summarize_docs
from db.init_db import ensure_movies_database_exists

from langchain_openai import ChatOpenAI

def init_db():
    ensure_movies_database_exists()

    cfg = load_config()
    df = load_sample("wiki_movie_plots_deduped.csv")
    docs = create_documents(df)
    embeddings = load_embedding_model()
    store = get_vector_store(embeddings, cfg["DB_CONNECTION"])
    add_documents_to_store(store,docs)

def run_query():
    cfg = load_config()
    embeddings = load_embedding_model()
    store = get_vector_store(embeddings, cfg["DB_CONNECTION"])
    query = "romantic movie with time travel"
    results = search_movies(store, query)
    summary = summarize_docs(results)
    print(summary)


if __name__ == "__main__":
    # import sys

    # if "--init-db" in sys.argv:
    #     init_db()
    # else:
    
    run_query()

    # init_db()
    # print(ChatOpenAI(model="gpt-4o-mini").invoke("Hello"))
