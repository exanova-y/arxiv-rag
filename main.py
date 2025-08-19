import arxiv
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
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


print("loading environment variables...")
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
llm = MistralAI(api_key=mistral_api_key, model='mistral-large-latest')

model_name = "mistral-embed"
embed_model = MistralAIEmbedding(model_name=model_name, api_key=mistral_api_key)
print("llm and embedding model set up.")

papers = fetch_arxiv_papers("cybersecurity", 3)
documents = create_documents_from_papers(papers)