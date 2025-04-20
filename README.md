# Movie QA System using LangChain, OpenAI Embeddings, and PGVector

This project implements a prototype movie identification and recommendation system using vector search (pgvector), LangChain for orchestration, and OpenAI embeddings. It uses an IMDb-style dataset with [Wikipedia plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) and returns structured recommendations powered by LLM output parsing.


---

## How to Replicate

Follow these steps to run the project locally.

### 1. Clone and Setup Environment
```bash
git clone https://github.com/yourusername/imdb_qa_pgvector_langchain.git
cd imdb_qa_pgvector_langchain
uv init  # or use your preferred environment manager
uv sync
```

### 2. Configure `.env`
Create a `.env` file in the root directory with the following content:
```
OPENAI_API_KEY=your_openai_key
DB_CONNECTION=postgresql+psycopg://postgres:mysecretpassword@localhost:5432/movies
```

### 3. Start Postgres with PGVector
Use Docker to spin up the Postgres container with PGVector:
```bash
docker run --name pgvector-container \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -d ankane/pgvector
```

> The project will automatically create the `movies` database if it doesn't exist.

### 4. Initialize Vector Store (Only Once)
```bash
python main.py --init-db
```

This loads a sample of movie plot data, generates embeddings, and stores them in the pgvector-backed database.

### 5. Run a Query
```bash
python main.py
```

Or use the programmatic API:
```python
from main import run_query

result = run_query("romantic movie with time travel")
print(result.json(indent=2))
```

---

## Architecture and Thought Process

This project is built to prototype a **scalable and extensible movie question-answering system** using vector search, structured LLM output, and robust software engineering practices. The architecture follows a clear separation of concerns to enable maintainability and future extensibility (e.g., integrating custom frontends or additional retrievers).


### 1. High-Level Flow

```
User Query
   ↓
Embeddings → Vector Search (PGVector)
   ↓
Documents (LangChain)
   ↓
Structured LLM Recommendation Output
   ↓
Pydantic Response Object
   ↓
Returned to User / Client
```


### 2. Modular Design Breakdown

The system is structured around the following key modules:

| Module | Responsibility |
|--------|----------------|
| `config/` | Loads `.env` environment variables such as OpenAI key and DB connection string |
| `data_loader/` | Loads and samples the movie plot dataset from CSV |
| `embedding/` | Loads and wraps the embedding model (`text-embedding-small`) |
| `db/` | Manages PostgreSQL and PGVector initialization, and database creation |
| `vector_store/` | Initializes the LangChain `PGVector` store using the embedding model |
| `query/search.py` | Runs semantic similarity search using the vector store |
| `query/formatter.py` | Transforms retrieved documents into structured `FinalRecommendation` objects via LLM |
| `schema/query_output.py` | Defines all Pydantic output models to standardize the shape of data |

Each module has a **single responsibility** and is designed to be testable, interchangeable, and reusable.

### 3. Why PGVector?

We chose **PGVector** (a PostgreSQL extension) as the vector store backend for several reasons:

- **Persistence & SQL Support**: Unlike in-memory or ephemeral vector databases (e.g., FAISS), PGVector allows long-term storage and querying using standard SQL.
- **Docker-native and lightweight**: Easily containerized with existing tooling, making it ideal for local and production deployments.
- **LangChain-native support**: Fully integrated with LangChain via `langchain_postgres`, which enables seamless chaining with embedding models and LLMs.
- **Ease of migration**: Since it’s PostgreSQL underneath, data and metadata can be easily migrated, queried, or exported using traditional tools.

### 4. Why Use `text-embedding-small`?

Although large embedding models like `text-embedding-3-large` offer high-quality representations, this system uses a **smaller embedding model (`text-embedding-small`)** for:

- **Faster processing**: Useful during rapid prototyping and low-latency pipelines.
- **Lower cost**: Optimized token cost per embedding when working with thousands of documents.
- **Sufficient quality**: The movie plot dataset is rich in contextual descriptions, and even smaller embeddings perform well in this domain.

The design is modular and allows for swapping in larger models later with minimal code changes.

### 5. Why This Schema?

The choice of Pydantic schema was guided by the principle of **minimal but expressive output** from the LLM and a **clean separation between data and reasoning**.

#### Breakdown:

| Schema | Purpose |
|--------|---------|
| `RecommendationFromLLM` | Captures the **model's reasoning** — why the result is relevant (`reason`) and what makes it unique (`highlights`) |
| `FinalRecommendation` | Adds back the original document metadata and `id` to retain context |
| `QueryResponse` | Wraps the full query + structured results for API responses or frontend consumption |

This schema offers the following benefits:

- **Decouples metadata from model-generated insight**.
- **Fully structured for JSON export, frontend rendering, or storage**.
- **Easy to test, serialize, and validate**.

This design makes the output human-readable yet machine-actionable — crucial for systems that need to serve users and downstream applications.

---

## Data Collection, Loading, and Building Vector DB

The dataset used is a cleaned version of the [Wikipedia Movie Plots dataset](https://www.cs.cmu.edu/~ark/personas/), which contains:

- `Release Year`, `Title`, `Origin`, `Genre`, `Director`, `Cast`, `Wiki Page`, and `Plot`

### Workflow

1. **CSV loading**:
   The dataset is read from `wiki_movie_plots_deduped.csv`.

2. **Random Sampling**:
   To optimize embedding cost and speed, only a random sample of 1000 records is loaded during database initialization.

3. **Document Creation**:
   Each movie is turned into a `langchain_core.Document` object with metadata such as title, genre, and origin.

4. **Embeddings**:
   OpenAI embeddings (`text-embedding-3-large`) are used to convert movie plots into vector representations.

5. **Vector Store**:
   The `langchain_postgres.PGVector` implementation is used to store vectors into PostgreSQL with the `pgvector` extension.

The entire setup is idempotent — it runs once and persists across queries.

---

## Structured Output

One of the key features of the system is its ability to return **structured recommendation responses**.

### Format

After retrieving relevant movies from the vector store, each result is sent to an LLM using LangChain's `with_structured_output()` method. The LLM is guided to extract:

- **Reason**: Why this movie is relevant to the user query.
- **Highlights**: Thematic tags extracted from the plot.

### Pydantic Schema

```python
class RecommendationFromLLM(BaseModel):
    reason: str
    highlights: List[str]

class FinalRecommendation(BaseModel):
    id: Union[int, str]
    metadata: dict
    structured: RecommendationFromLLM

class QueryResponse(BaseModel):
    query: str
    recommendations: List[FinalRecommendation]
```

### Example Output

```json
{
  "query": "romantic movie with time travel",
  "recommendations": [
    {
      "id": "144",
      "metadata": {
        "title": "The Age of Adaline",
        "year": 2015,
        ...
      },
      "structured": {
        "reason": "Explores the tension of immortality and love, featuring a woman who doesn't age due to a freak accident and her struggle to maintain relationships.",
        "highlights": ["immortality", "romance", "identity", "sacrifice"]
      }
    }
  ]
}
```

This structured format allows downstream applications to cleanly parse and present LLM-generated insights alongside original metadata.

---

Let me know if you'd like to generate badges (e.g. Python version, license) or add a section on evaluation/future directions.