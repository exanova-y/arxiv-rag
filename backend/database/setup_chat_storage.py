import os
import dotenv
from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

# Grab from environment
dotenv.load_dotenv()
db_url = (
    os.getenv("DATABASE_URL")
    or os.getenv("DATABASE_PUBLIC_URL")
)

# If not provided, build from component vars with sane defaults - railway
if not db_url:
    host = os.getenv("PGHOST") or os.getenv("POSTGRES_HOST") or "127.0.0.1"
    port = os.getenv("PGPORT") or os.getenv("POSTGRES_PORT") or "5432"
    user = os.getenv("PGUSER") or os.getenv("POSTGRES_USER") or "postgres"
    password = os.getenv("PGPASSWORD") or os.getenv("POSTGRES_PASSWORD") or "password"
    database = os.getenv("PGDATABASE") or os.getenv("POSTGRES_DB") or "arxiv_rag"
    db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

# Normalize scheme to async driver expected by LlamaIndex PostgresChatStore
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

use_pg_chat = os.getenv("USE_PG_CHAT", "1") == "1"
chat_store = None
if use_pg_chat and db_url:
    # Create chat store with Postgres (async engine)
    chat_store = PostgresChatStore.from_uri(uri=db_url)

if chat_store:
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key="user1",
    )
else:
    # Fallback: in-memory chat (no Postgres env configured)
    chat_memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
