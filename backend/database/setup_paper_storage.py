# note: this script includes one additional step, which is converting embeddings into rows rather than text to rows. this results in unreadable data. 
# run build_index.py to directly convert paper text into rows.

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.llms.mistralai import MistralAI

import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import make_url


load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=mistral_api_key)

# psycopg2 is a PostgreSQL adapter for Python. it's a low-level, direct way to talk to Postgres 
print("creating db.")
db_url = os.getenv("DATABASE_URL")
db_name = "arxiv_rag"
conn = psycopg2.connect(db_url)
conn.autocommit = True

# sqlalchemy is a database toolkit for Python. 
# 1 it has a nice API to build SQL queries programmatically (instead of writing raw strings).
# 2 it maps python classes to database tables (object-relational mapping).
url = make_url(db_url)

# A query is another vector and you want the “closest” ones
# HNSW is a graph-based algorithm for fast nearest-neighbor search.
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="arxiv_papers",
    embed_dim=1024,  # Mistral embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16, # number of neighbors each node links to
        "hnsw_ef_construction": 64, # how much effort to spend building the index (higher = slower build, better quality).
        "hnsw_ef_search": 40, # how much effort to spend searching (higher = slower queries, more accurate).
        "hnsw_dist_method": "vector_cosine_ops", # cosine similarity
    },
)

# Load documents from index directory  
index_path = "../../index"  # Simple relative path
documents = SimpleDirectoryReader(index_path).load_data()
print(f"Loaded {len(documents)} documents")

# this seems duplicated, may delete soon.
conn_db = psycopg2.connect(db_url)
conn_db.autocommit = True
with conn_db.cursor() as c:
    c.execute("CREATE EXTENSION IF NOT EXISTS vector;")
print("pgvector extension enabled")

# Create PostgreSQL index with documents
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model, show_progress=True) # PGVectorStore automatically creates table of arxiv papers.

print("PostgreSQL index created!")