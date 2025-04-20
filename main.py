from config import load_config
from data.load_data import load_sample
from data.preprocess import create_documents
from db.vector_store import get_vector_store, add_documents_to_store
from embedding.embed import load_embedding_model
from query.search import search_movies
from query.formatter import format_query_results
from db.init_db import ensure_movies_database_exists
from schema.query_output import QueryResponse

def init_db():
    ensure_movies_database_exists()

    cfg = load_config()
    df = load_sample("wiki_movie_plots_deduped.csv")
    docs = create_documents(df)
    embeddings = load_embedding_model()
    store = get_vector_store(embeddings, cfg["DB_CONNECTION"])
    add_documents_to_store(store,docs)

def run_query(user_query: str, k: int = 5) -> QueryResponse:
    # Load config and setup
    cfg = load_config()
    embeddings = load_embedding_model()
    store = get_vector_store(embeddings, cfg["DB_CONNECTION"])

    # Run similarity search
    docs = search_movies(store, user_query, k=k)

    # Format using LLM + structured output schema
    structured_result = format_query_results(user_query, docs)

    return structured_result


if __name__ == "__main__":
    query = "action packed mordern movie"
    result = run_query(query)
    
    # Print to console
    print(result.model_dump_json(indent=2))

    # Optional: Save to file
    with open("query_result.json", "w") as f:
        f.write(result.model_dump_json(indent=2))
