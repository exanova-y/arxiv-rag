# copy pasted from build_index.py
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, load_index_from_storage, PromptTemplate, Settings
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.agent.workflow import ReActAgent # the import source has changed
from llama_index.core.workflow import Context

import os 
import requests
from dotenv import load_dotenv
import asyncio

from rich.console import Console
from rich.markdown import Markdown

from build_index import fetch_arxiv_tool

# Setup query engine at module level
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
llm = MistralAI(api_key=mistral_api_key, model='mistral-large-latest')

model_name = "mistral-embed"
embed_model = MistralAIEmbedding(model_name=model_name, api_key=mistral_api_key)

print("loading index")
storage_context = StorageContext.from_defaults(persist_dir='index/')
index = load_index_from_storage(storage_context, embed_model=embed_model)

print("building query engine")
query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

setup_query_engine()
agent = ReActAgent(tools=[download_pdf_tool, rag_tool, fetch_arxiv_tool], llm=llm, verbose=True)
ctx = Context(agent)

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

rag_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="research_paper_query_engine_tool",
    description="A RAG engine with some research papers.",)
    

def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}" f" **Text:** "
        console.print(Markdown(text_md))
        console.print(p.get_template())
        console.print(Markdown(""))

#display_prompt_dict(prompts_dict)


def setup_query_engine():
    # actually, system level prompts are optional.
    print("preparing system-level prompts for search and refinement")
    prompts_dict = query_engine.get_prompts()
    print(prompts_dict)
    print('done printing.')
    console = Console()  

    return rag_tool  


if __name__ == "__main__":
    agent, ctx = setup_agent()
