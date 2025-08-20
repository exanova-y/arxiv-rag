Pre-requisites:
- PostgreSQL
- pgvector
on mac, you can use brew to install the above.

(to be updated)


Process
- Build index stores papers inside index. the important files are docstore.json, where you can roughly estimate how many papers there are.
- Agent searches local RAG index first.
- If NO RELEVANT PAPERS, automatically calls fetch_arxiv_tool to get some new papers. 
- Users can use [refine mode](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/). The agent is equipped with a standard rag tool and a refine rag tool. The user should specifically ask for using research_paper_refine_tool. This could be a dropdown that could be selected in the UI.


Notes
- Currently using Mistral. Need to install llama-index-llms-anthropic for claude support

