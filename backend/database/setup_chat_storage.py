import os
import dotenv
from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

# Grab from environment
dotenv.load_dotenv()
db_url = os.getenv("DATABASE_URL")
print(db_url)

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
