import os
from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

# Grab from environment
db_url = os.getenv("DATABASE_URL")

# Railway sometimes gives "postgres://", but SQLAlchemy / asyncpg need "postgresql+asyncpg://"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
# Under the hood it uses SQLAlchemy async, so it does need postgresql+asyncpg://...???


# Create chat store with Railway DB
chat_store = PostgresChatStore.from_uri(
    uri=db_url,
)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
