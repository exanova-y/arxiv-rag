# copy pasted from build_index.py
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, load_index_from_storage, PromptTemplate, Settings
from llama_index.core.tools import FunctionTool, QueryEngineTool
import os 
from dotenv import load_dotenv

from rich.console import Console
from rich.markdown import Markdown

# common set up.
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
llm = MistralAI(api_key=mistral_api_key, model='mistral-large-latest')

model_name = "mistral-embed"
embed_model = MistralAIEmbedding(model_name=model_name, api_key=mistral_api_key)



print("loading index")
storage_context = StorageContext.from_defaults(persist_dir='index/')
index = load_index_from_storage(storage_context, embed_model=embed_model)
print(index)


print("building query engine")
query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)
rag_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="research_paper_query_engine_tool",
    description="A RAG engine with some research papers.",
)

prompts_dict = query_engine.get_prompts()
print(prompts_dict)
print('done printing.')
console = Console()

def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}" f" **Text:** "
        console.print(Markdown(text_md))
        console.print(p.get_template())
        console.print(Markdown(""))

display_prompt_dict(prompts_dict)