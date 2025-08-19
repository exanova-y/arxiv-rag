

Process
- Agent searches local RAG index first.
- If NO RELEVANT PAPERS, automatically calls fetch_arxiv_tool to get some new papers. 

Notes
- Need to install llama-index-llms-anthropic for claude support