# copy pasted from build_index.py
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, load_index_from_storage, PromptTemplate, Settings
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.agent.workflow import ReActAgent # the import source has changed
from llama_index.core.workflow import Context

from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore

import os
from dotenv import load_dotenv
import requests

from rich.console import Console
from rich.markdown import Markdown

# absolute imports
from build_index import fetch_arxiv_tool
from database.setup_chat_storage import chat_memory

def download_pdf(pdf_url, output_file):
    response = requests.get(pdf_url)
    response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)
    return f"PDF downloaded successfully and saved as '{output_file}'."

# wraps the python function for llama-index
download_pdf_tool = FunctionTool.from_defaults(
    download_pdf,
    name='download_pdf_file_tool',
    description='python function, which downloads a pdf file by link'
)

def display_prompt_dict(prompts_dict):
    console = Console()  
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}" f" **Text:** "
        console.print(Markdown(text_md))
        console.print(p.get_template())
        console.print(Markdown(""))

#display_prompt_dict(prompts_dict)

# Moved out of function to set up query engine at module level
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
llm = MistralAI(api_key=mistral_api_key, model='mistral-large-latest')

model_name = "mistral-embed"
embed_model = MistralAIEmbedding(model_name=model_name, api_key=mistral_api_key)


print("loading index")

# Use PostgreSQL PGVectorStore only
db_url = os.getenv("DATABASE_URL")
url = make_url(connection_string)

if not db_name:
    db_name = url.database or "arxiv_rag"

table_name = os.getenv("PGVECTOR_TABLE", "arxiv_papers")
print(f"Using PGVector table: {table_name} on {url.host}:{url.port}/{db_name}")

vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name=table_name,
    embed_dim=1024,
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)



print("building query engine")
query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)
query_engine_refine = index.as_query_engine(llm=llm, similarity_top_k=10, response_mode='refine')

# to use refine, 
# we create two rag tools for both search "text_qa_template" and refine "refine_template"
# and give both tools to the agent
print("creating standard and refine rag tools")
rag_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="research_paper_query_engine_tool",
    description="A RAG engine with research papers. Use for standard queries.",)

rag_tool_refine = QueryEngineTool.from_defaults(
    query_engine_refine,
    name="research_paper_refine_tool", 
    description="A RAG engine that provides refined answers for research papers. Please use when the user follows up with above queries for more interesting, specific information.",)

# are system level prompts optional?
print("preparing system-level prompts for search and refinement")
prompts_dict = query_engine.get_prompts()
display_prompt_dict(prompts_dict)
print('done printing.')

print("building a 'Reasoning and Acting' agent which has 4 tools")
# Reasoning: Upon receiving a query, the agent evaluates whether it has enough information to answer directly or if it needs to use a tool.
# Acting: If the agent decides to use a tool, it executes the tool and then returns to the Reasoning stage to determine whether it can now answer the query or if further tool usage is necessary.

agent = ReActAgent(tools=[download_pdf_tool, rag_tool, rag_tool_refine, fetch_arxiv_tool], llm=llm, verbose=True, memory=chat_memory)
ctx = Context(agent)

if __name__ == "__main__":
    print("build_query_engine ready. Tools: research_paper_query_engine_tool, research_paper_refine_tool, fetch_arxiv_tool")
