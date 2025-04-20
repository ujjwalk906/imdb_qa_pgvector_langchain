## How to Replicate

1. **Setup Environment**:
   - Ensure you have Python 3.12 installed. You can use the `.python-version` file to set up the correct version with tools like `pyenv`.
   - Install dependencies using `pip`:
     ```bash
     pip install -r requirements.txt
     ```
   - Create a [.env](http://_vscodecontentref_/0) file with necessary environment variables (e.g., database connection details).

2. **Initialize Database**:
   - Run the [init_db](http://_vscodecontentref_/1) function in [main.py](http://_vscodecontentref_/2) to set up the database and populate it with movie data:
     ```bash
     python main.py
     ```

3. **Run Queries**:
   - Use the [run_query](http://_vscodecontentref_/3) function in [main.py](http://_vscodecontentref_/4) to perform similarity searches on the vector database:
     ```bash
     python main.py
     ```

4. **View Results**:
   - The query results will be printed to the console and saved to [query_result.json](http://_vscodecontentref_/5).

---

## Architecture and Thought Process

This project is designed to enable semantic search over a movie dataset using vector embeddings and a structured output format. The architecture is modular, with clear separation of concerns:

1. **Data Layer**:
   - The [data](http://_vscodecontentref_/6) module handles loading ([load_data.py](http://_vscodecontentref_/7)) and preprocessing ([preprocess.py](http://_vscodecontentref_/8)) of the movie dataset.

2. **Database Layer**:
   - The [db](http://_vscodecontentref_/9) module manages database initialization ([init_db.py](http://_vscodecontentref_/10)) and vector storage ([vector_store.py](http://_vscodecontentref_/11)) using pgvector.

3. **Embedding Layer**:
   - The [embedding](http://_vscodecontentref_/12) module ([embed.py](http://_vscodecontentref_/13)) loads and manages the embedding model for vectorization.

4. **Query Layer**:
   - The [query](http://_vscodecontentref_/14) module handles search ([search.py](http://_vscodecontentref_/15)), formatting results ([formatter.py](http://_vscodecontentref_/16)), and summarizing (`summarize.py`).

5. **Schema Layer**:
   - The [schema](http://_vscodecontentref_/17) module ([query_output.py](http://_vscodecontentref_/18)) defines the structured output format for query results.

6. **Main Script**:
   - The [main.py](http://_vscodecontentref_/19) script orchestrates the workflow, from database initialization to query execution.

---

## Data Collection, Loading, And Building Vector DB

1. **Data Collection**:
   - The dataset [wiki_movie_plots_deduped.csv](http://_vscodecontentref_/20) contains movie plots and metadata.

2. **Data Loading**:
   - The [load_sample](http://_vscodecontentref_/21) function in [load_data.py](http://_vscodecontentref_/22) reads the dataset into a DataFrame.

3. **Preprocessing**:
   - The [create_documents](http://_vscodecontentref_/23) function in [preprocess.py](http://_vscodecontentref_/24) converts the DataFrame into a format suitable for embedding.

4. **Building Vector DB**:
   - The [init_db](http://_vscodecontentref_/25) function in [main.py](http://_vscodecontentref_/26) ensures the database is initialized.
   - Embeddings are generated using the [load_embedding_model](http://_vscodecontentref_/27) function in [embed.py](http://_vscodecontentref_/28).
   - The [add_documents_to_store](http://_vscodecontentref_/29) function in [vector_store.py](http://_vscodecontentref_/30) stores the embeddings in the vector database.

---

## Structured Output

The project uses a structured output format for query results, defined in [query_output.py](http://_vscodecontentref_/31). The [QueryResponse](http://_vscodecontentref_/32) schema ensures consistency and readability of results.

1. **Query Execution**:
   - The [run_query](http://_vscodecontentref_/33) function in [main.py](http://_vscodecontentref_/34) performs a similarity search using the [search_movies](http://_vscodecontentref_/35) function in [search.py](http://_vscodecontentref_/36).

2. **Formatting Results**:
   - The [format_query_results](http://_vscodecontentref_/37) function in [formatter.py](http://_vscodecontentref_/38) combines the query and search results into a structured format.

3. **Output Example**:
   - Results are printed to the console and saved to [query_result.json](http://_vscodecontentref_/39) in JSON format:
     ```json
     {
       "query": "action packed modern movie",
       "results": [
         {
           "title": "Movie Title",
           "plot": "Movie plot summary...",
           "similarity_score": 0.95
         }
       ]
     }
     ```