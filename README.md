(to be updated)



Process
- Build index stores papers inside index. the important files are docstore.json, where you can roughly estimate how many papers there are.
- Agent searches local RAG index first.
- If NO RELEVANT PAPERS, automatically calls fetch_arxiv_tool to get some new papers. 


Notes
- Currently using Mistral. Need to install llama-index-llms-anthropic for claude support