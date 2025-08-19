import arxiv
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document, StorageContext, load_index_from_storage, PromptTemplate, Settings
from llama_index.core.tools import FunctionTool, QueryEngineTool
import os
from dotenv import load_dotenv


# define paper download
def fetch_arxiv_papers(title :str, papers_count: int):
    search_query = f'all:"{title}"'
    search = arxiv.Search(
        query=search_query,
        max_results=papers_count,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    # Use the Client for searching
    client = arxiv.Client()
    
    # Execute the search
    search = client.results(search)

    for result in search:
        paper_info = {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'summary': result.summary,
                'published': result.published,
                'journal_ref': result.journal_ref,
                'doi': result.doi,
                'primary_category': result.primary_category,
                'categories': result.categories,
                'pdf_url': result.pdf_url,
                'arxiv_url': result.entry_id
            }
        papers.append(paper_info)

    return papers

# wraps the function for llama-index
fetch_arxiv_tool = FunctionTool.from_defaults(
    fetch_arxiv_papers,
    name='fetch_from_arxiv',
    description='download the {max_results} recent papers regarding the topic {title} from arxiv' 
)

def create_documents_from_papers(papers):
    documents = []
    for paper in papers:
        content = f"Title: {paper['title']}\n" \
                  f"Authors: {', '.join(paper['authors'])}\n" \
                  f"Summary: {paper['summary']}\n" \
                  f"Published: {paper['published']}\n" \
                  f"Journal Reference: {paper['journal_ref']}\n" \
                  f"DOI: {paper['doi']}\n" \
                  f"Primary Category: {paper['primary_category']}\n" \
                  f"Categories: {', '.join(paper['categories'])}\n" \
                  f"PDF URL: {paper['pdf_url']}\n" \
                  f"arXiv URL: {paper['arxiv_url']}\n"
        documents.append(Document(text=content))
    return documents


# Only execute when run directly, not when imported
if __name__ == "__main__":
    print("loading environment variables...")
    load_dotenv()
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    llm = MistralAI(api_key=mistral_api_key, model='mistral-large-latest')

    model_name = "mistral-embed"
    embed_model = MistralAIEmbedding(model_name=model_name, api_key=mistral_api_key)
    print("llm and embedding model set up.")

    papers = fetch_arxiv_papers("cybersecurity OR IT security OR infosec OR network security", 50)
    documents = create_documents_from_papers(papers)
    print("documents created.")
    print([[p['title']] for p in papers])

    print("definiing chunk settings")
    Settings.chunk_size = 1024 # the specified maximum num characters per text chunk
    Settings.chunk_overlap = 50 # (specified) maximum num characters of overlap between chunks
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # store the index to avoid re-indexing. 
    # for now, just store thtese indices locally inside a dir.
    print("storing indices")
    index.storage_context.persist('index/') # saves indices locally
    storage_context = StorageContext.from_defaults(persist_dir='index/')
    index = load_index_from_storage(storage_context, embed_model=embed_model)
    print(index)
