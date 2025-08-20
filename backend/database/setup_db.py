from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore

import textwrap
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import make_url


print("creating db.")
# create the database
connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "arxiv_rag"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

# # create vector store with database connection
# url = make_url(connection_string)
# vector_store = PGVectorStore.from_params(
#     database=db_name,
#     host=url.host,
#     password=url.password,
#     port=url.port,
#     user=url.username,
#     table_name="arxiv_papers",
#     embed_dim=1024,  # Mistral embedding dimension
#     hnsw_kwargs={
#         "hnsw_m": 16,
#         "hnsw_ef_construction": 64,
#         "hnsw_ef_search": 40,
#         "hnsw_dist_method": "vector_cosine_ops",
#     },
# )