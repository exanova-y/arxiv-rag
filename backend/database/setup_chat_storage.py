from llama_index.storage.chat_store.postgres import PostgresChatStore
from llama_index.core.memory import ChatMemoryBuffer

# using the same db, but creating separate tables
chat_store = PostgresChatStore.from_uri(
    uri="postgresql+asyncpg://postgres:password@127.0.0.1:5432/arxiv_rag",
)

chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)

# I think no persist methods are required.